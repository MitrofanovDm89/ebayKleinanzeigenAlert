import sys
import logging
from random import randint
from time import sleep
from sqlalchemy.orm import Session
from ebAlert import create_logger
from ebAlert.crud.base import crud_link, get_session
from ebAlert.crud.post import crud_post
from ebAlert.ebayscrapping import ebayclass
from ebAlert.telegram.telegramclass import telegram

# Настройка логирования
log = create_logger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

try:
    import click
    from click import BaseCommand
except ImportError:
    log.error("Click should be installed\npip install click")


@click.group()
def cli() -> BaseCommand:
    pass


@cli.command(help="Запустить сбор объявлений и отправку в Telegram.")
def start():
    """
    Обходит все ссылки в БД, парсит объявления и отправляет в Telegram.
    """
    print(">> Запуск Ebay Alert...")
    with get_session() as db:
        get_all_post(db=db, telegram_message=True)
    print("<< Ebay Alert завершен.")


@cli.command(options_metavar="<options>", help="Добавить/Просмотреть/Удалить ссылки из БД.")
@click.option("-r", "--remove_link", 'remove', metavar="<link id>", help="Удалить ссылку из базы.")
@click.option("-c", "--clear", is_flag=True, help="Очистить базу объявлений.")
@click.option("-a", "--add_url", 'url', metavar='<URL>', help="Добавить ссылку в БД и загрузить объявления.")
@click.option("-i", "--init", is_flag=True, help="Инициализировать базу данных.")
@click.option("-s", "--show", is_flag=True, help="Показать все ссылки и их ID.")
def links(show, remove, clear, url, init):
    """
    Управление ссылками в базе данных: добавление, удаление, просмотр.
    """
    with get_session() as db:
        if show:
            print(">> Список ссылок в базе:")
            links = crud_link.get_all(db)
            if links:
                for link_model in links:
                    print(f"{link_model.id}: {link_model.link}")
            print("<< Конец списка ссылок.")

        elif remove:
            print(">> Удаление ссылки...")
            if crud_link.remove(db=db, id=remove):
                print("<< Ссылка удалена.")
            else:
                print("<< Ссылка не найдена.")

        elif clear:
            print(">> Очистка базы объявлений...")
            crud_post.clear_database(db=db)
            print("<< База очищена.")

        elif url:
            print(">> Добавление ссылки...")
            if crud_link.get_by_key(key_mapping={"link": url}, db=db):
                print("<< Ссылка уже существует.")
                return  # Прерываем выполнение, если ссылка уже есть

            # Добавляем ссылку в БД
            crud_link.create({"link": url}, db)
            ebay_items = ebayclass.EbayItemFactory(url)
            items_added = crud_post.add_items_to_db(db, ebay_items.item_list)

            print(f"<< Добавлено объявлений: {len(items_added)}")
            for item in items_added:
                print(f"  - {item.title}")  # Вывод названий объявлений

        elif init:
            print(">> Инициализация базы...")
            get_all_post(db)
            print("<< База инициализирована.")


def get_all_post(db: Session, telegram_message=False):
    """
    Проходит по всем ссылкам в базе, получает объявления и отправляет в Telegram.
    """
    links = crud_link.get_all(db=db)
    if links:
        for link_model in links:
            print(f"🔍 Обрабатывается: {link_model.link}")
            post_factory = ebayclass.EbayItemFactory(link_model.link)

            # Логируем количество найденных объявлений
            found_items = post_factory.item_list
            print(f"✅ Найдено объявлений: {len(found_items)}")

            if found_items:
                for item in found_items:
                    print(f"  - {item.title}")  # Вывод заголовков объявлений

            items = crud_post.add_items_to_db(db=db, items=found_items)

            # Отправка в Telegram
            if telegram_message and items:
                for item in items:
                    print(f"📩 Отправка в Telegram: {item.title}")
                    log.info(f"📩 Отправка объявления: {item.title} в Telegram")
                    telegram.send_formated_message(item)

            sleep(randint(3, 8))  # Задержка перед следующим запросом


@cli.command(help="Запустить Telegram-бота.")
def telegram_bot():
    """
    Запуск Telegram-бота для управления ссылками через Telegram.
    """
    try:
        from ebAlert.telegram.telegram_bot import main as run_telegram_bot
        print("✅ Запуск Telegram-бота...")
        run_telegram_bot()
    except ImportError as e:
        log.error(f"Ошибка импорта Telegram-бота: {e}")
        print("⚠️ Не удалось запустить Telegram-бота. Проверь зависимости.")
        sys.exit(1)


if __name__ == "__main__":
    cli(sys.argv[1:])
