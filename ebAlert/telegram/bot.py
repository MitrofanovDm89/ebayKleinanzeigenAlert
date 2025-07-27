import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters
from telegram.constants import ParseMode

from ebAlert.core.config import settings
from ebAlert.crud.base import get_session, crud_link
from ebAlert.crud.post import crud_post
from ebAlert.crud.user import crud_user, crud_user_filter
from ebAlert.ebayscrapping.ebayclass import EbayItemFactory
from ebAlert.models.sqlmodel import EbayLink
from ebAlert.models.user_models import User

# Состояния для ConversationHandler
CHOOSING_ACTION, ADDING_FILTER, EDITING_FILTER, REMOVING_FILTER = range(4)

class ClientInsightingBot:
    def __init__(self):
        self.application = Application.builder().token(settings.TOKEN).build()
        self.setup_handlers()
        self.logger = logging.getLogger(__name__)
        
    def setup_handlers(self):
        """Настройка обработчиков команд"""
        
        # Основные команды
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("filters", self.show_filters))
        self.application.add_handler(CommandHandler("add_filter", self.add_filter_start))
        self.application.add_handler(CommandHandler("remove_filter", self.remove_filter_start))
        self.application.add_handler(CommandHandler("check_now", self.check_now))
        
        # Conversation handler для добавления фильтров
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("add_filter", self.add_filter_start)],
            states={
                ADDING_FILTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.add_filter_process)]
            },
            fallbacks=[CommandHandler("cancel", self.cancel)]
        )
        self.application.add_handler(conv_handler)
        
        # Обработчик inline кнопок
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
    async def start_command(self, update: Update, context):
        """Обработчик команды /start"""
        # Получаем или создаем пользователя
        user_info = update.effective_user
        with get_session() as db:
            user = crud_user.create_or_get_user(
                telegram_id=user_info.id,
                username=user_info.username,
                first_name=user_info.first_name,
                last_name=user_info.last_name,
                db=db
            )
        
        welcome_text = f"""
🤖 **Client Insighting Bot**

Привет, {user_info.first_name or user_info.username or 'пользователь'}! 

Я помогу вам отслеживать новые объявления на eBay Kleinanzeigen.

**Доступные команды:**
• `/filters` - Показать ваши фильтры
• `/add_filter` - Добавить новый фильтр
• `/remove_filter` - Удалить фильтр
• `/check_now` - Проверить новые объявления сейчас
• `/help` - Показать справку

**Как добавить фильтр:**
1. Скопируйте URL поиска с eBay Kleinanzeigen
2. Используйте команду `/add_filter`
3. Вставьте URL в следующем сообщении

Начните с добавления первого фильтра!
        """
        
        keyboard = [
            [InlineKeyboardButton("📋 Мои фильтры", callback_data="show_filters")],
            [InlineKeyboardButton("➕ Добавить фильтр", callback_data="add_filter")],
            [InlineKeyboardButton("🔍 Проверить сейчас", callback_data="check_now")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
        
    async def help_command(self, update: Update, context):
        """Обработчик команды /help"""
        help_text = """
📚 **Справка по использованию бота**

**Основные команды:**
• `/start` - Главное меню
• `/filters` - Показать все ваши фильтры
• `/add_filter` - Добавить новый фильтр поиска
• `/remove_filter` - Удалить фильтр
• `/check_now` - Проверить новые объявления

**Как создать фильтр:**
1. Зайдите на eBay Kleinanzeigen
2. Настройте поиск (категория, цена, местоположение и т.д.)
3. Скопируйте URL из адресной строки
4. Используйте команду `/add_filter` и вставьте URL

**Примеры фильтров:**
• Поиск автомобилей в определенном городе
• Товары в определенном ценовом диапазоне
• Конкретная категория товаров

**Уведомления:**
Бот будет автоматически проверять новые объявления каждые 30 минут и отправлять уведомления о новых предложениях.
        """
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
        
    async def show_filters(self, update: Update, context):
        """Показать все фильтры пользователя"""
        await self._show_filters_list(update, context)
        
    async def _show_filters_list(self, update: Update, context):
        """Внутренний метод для показа фильтров"""
        user_info = update.effective_user
        
        with get_session() as db:
            # Получаем пользователя
            user = crud_user.get_by_telegram_id(user_info.id, db)
            if not user:
                await self._send_error_message(update, "Пользователь не найден. Попробуйте /start")
                return
                
            # Получаем фильтры пользователя
            filters = crud_user_filter.get_user_filters(user.id, db)
            
        if not filters:
            text = "📭 У вас пока нет добавленных фильтров.\n\nИспользуйте `/add_filter` для добавления первого фильтра."
            keyboard = [[InlineKeyboardButton("➕ Добавить фильтр", callback_data="add_filter")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if hasattr(update, 'callback_query'):
                await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
            else:
                await update.message.reply_text(text, reply_markup=reply_markup)
            return
            
        text = "📋 **Ваши фильтры:**\n\n"
        keyboard = []
        
        for i, filter_item in enumerate(filters, 1):
            # Показываем название фильтра или URL
            display_name = filter_item.name or filter_item.url[:50] + "..." if len(filter_item.url) > 50 else filter_item.url
            text += f"{i}. **{display_name}**\n"
            if filter_item.name:
                text += f"   `{filter_item.url[:50]}{'...' if len(filter_item.url) > 50 else ''}`\n"
            keyboard.append([InlineKeyboardButton(f"❌ Удалить {i}", callback_data=f"remove_{filter_item.id}")])
            
        keyboard.append([InlineKeyboardButton("➕ Добавить фильтр", callback_data="add_filter")])
        keyboard.append([InlineKeyboardButton("🔍 Проверить сейчас", callback_data="check_now")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if hasattr(update, 'callback_query'):
            await update.callback_query.edit_message_text(
                text, 
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                text, 
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
            
    async def add_filter_start(self, update: Update, context):
        """Начало процесса добавления фильтра"""
        text = """
➕ **Добавление нового фильтра**

Пожалуйста, отправьте URL поиска с eBay Kleinanzeigen.

**Как получить URL:**
1. Зайдите на eBay Kleinanzeigen
2. Настройте поиск (категория, цена, местоположение)
3. Скопируйте URL из адресной строки браузера
4. Отправьте его в следующем сообщении

**Пример URL:**
`https://www.kleinanzeigen.de/s-autos/c216`

Отправьте URL или нажмите "Отмена" для возврата в главное меню.
        """
        
        keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data="cancel")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if hasattr(update, 'callback_query'):
            await update.callback_query.edit_message_text(
                text, 
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                text, 
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
            
        return ADDING_FILTER
        
    async def add_filter_process(self, update: Update, context):
        """Обработка добавления фильтра"""
        url = update.message.text.strip()
        user_info = update.effective_user
        
        # Простая валидация URL
        if not url.startswith("https://www.kleinanzeigen.de"):
            await update.message.reply_text(
                "❌ Неверный URL! URL должен начинаться с `https://www.kleinanzeigen.de`",
                parse_mode=ParseMode.MARKDOWN
            )
            return ConversationHandler.END
            
        try:
            with get_session() as db:
                # Получаем или создаем пользователя
                user = crud_user.get_by_telegram_id(user_info.id, db)
                if not user:
                    await self._send_error_message(update, "Пользователь не найден. Попробуйте /start")
                    return ConversationHandler.END
                
                # Проверяем, не существует ли уже такой фильтр у пользователя
                existing_filter = crud_user_filter.get_by_url_and_user(url, user.id, db)
                if existing_filter:
                    await update.message.reply_text("⚠️ Этот фильтр уже добавлен!")
                    return ConversationHandler.END
                    
                # Добавляем фильтр для пользователя
                filter_obj = crud_user_filter.create_user_filter(user.id, url, db=db)
                
                # Проверяем, что URL работает и получаем первые объявления
                try:
                    ebay_items = EbayItemFactory(url)
                    if ebay_items.item_list:
                        crud_post.add_items_to_db(db, ebay_items.item_list)
                        await update.message.reply_text(
                            f"✅ Фильтр успешно добавлен!\n\n"
                            f"Найдено {len(ebay_items.item_list)} существующих объявлений.\n"
                            f"Теперь вы будете получать уведомления о новых объявлениях.",
                            parse_mode=ParseMode.MARKDOWN
                        )
                    else:
                        await update.message.reply_text(
                            "⚠️ Фильтр добавлен, но не удалось получить объявления.\n"
                            "Возможно, URL некорректный или нет результатов поиска."
                        )
                except Exception as e:
                    self.logger.error(f"Error processing URL {url}: {e}")
                    await update.message.reply_text(
                        "⚠️ Фильтр добавлен, но произошла ошибка при проверке объявлений.\n"
                        "Попробуйте проверить URL вручную."
                    )
                    
        except Exception as e:
            self.logger.error(f"Error adding filter: {e}")
            await update.message.reply_text("❌ Произошла ошибка при добавлении фильтра.")
            
        return ConversationHandler.END
        
    async def remove_filter_start(self, update: Update, context):
        """Начало процесса удаления фильтра"""
        await self._show_filters_list(update, context)
        
    async def check_now(self, update: Update, context):
        """Проверить новые объявления сейчас"""
        user_info = update.effective_user
        
        await update.message.reply_text("🔍 Проверяю новые объявления...")
        
        new_items = []
        with get_session() as db:
            # Получаем пользователя
            user = crud_user.get_by_telegram_id(user_info.id, db)
            if not user:
                await self._send_error_message(update, "Пользователь не найден. Попробуйте /start")
                return
                
            # Получаем фильтры пользователя
            filters = crud_user_filter.get_user_filters(user.id, db)
            
            if not filters:
                await update.message.reply_text("📭 У вас нет добавленных фильтров.")
                return
                
            for filter_item in filters:
                try:
                    ebay_items = EbayItemFactory(filter_item.url)
                    items = crud_post.add_items_to_db(db=db, items=ebay_items.item_list)
                    new_items.extend(items)
                except Exception as e:
                    self.logger.error(f"Error checking filter {filter_item.url}: {e}")
                    
        if new_items:
            await update.message.reply_text(f"🎉 Найдено {len(new_items)} новых объявлений!")
            
            # Отправляем уведомления о новых объявлениях
            for item in new_items[:5]:  # Ограничиваем первыми 5 объявлениями
                await self._send_item_notification(update, item)
                
            if len(new_items) > 5:
                await update.message.reply_text(f"... и еще {len(new_items) - 5} объявлений.")
        else:
            await update.message.reply_text("📭 Новых объявлений не найдено.")
            
    async def _send_item_notification(self, update: Update, item):
        """Отправка уведомления об объявлении"""
        message = f"""
🆕 **Новое объявление!**

📌 **{item.title}**

💰 **Цена:** {item.price}
📍 **Местоположение:** {item.city}
📝 **Описание:** {item.description[:100]}{'...' if len(item.description) > 100 else ''}

🔗 [Открыть объявление]({item.link})
        """
        
        keyboard = [[InlineKeyboardButton("🔗 Открыть", url=item.link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
        
    async def button_callback(self, update: Update, context):
        """Обработчик нажатий на inline кнопки"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "show_filters":
            await self._show_filters_list(update, context)
        elif query.data == "add_filter":
            await self.add_filter_start(update, context)
        elif query.data == "check_now":
            await self.check_now(update, context)
        elif query.data == "cancel":
            await query.edit_message_text("❌ Операция отменена.")
        elif query.data.startswith("remove_"):
            filter_id = int(query.data.split("_")[1])
            await self._remove_filter(update, context, filter_id)
            
    async def _remove_filter(self, update: Update, context, filter_id: int):
        """Удаление фильтра"""
        user_info = update.effective_user
        
        with get_session() as db:
            # Получаем пользователя
            user = crud_user.get_by_telegram_id(user_info.id, db)
            if not user:
                await self._send_error_message(update, "Пользователь не найден. Попробуйте /start")
                return
                
            # Удаляем фильтр пользователя
            if crud_user_filter.deactivate_filter(filter_id, user.id, db):
                await update.callback_query.edit_message_text("✅ Фильтр успешно удален!")
            else:
                await update.callback_query.edit_message_text("❌ Фильтр не найден.")
                
    async def cancel(self, update: Update, context):
        """Отмена операции"""
        await update.message.reply_text("❌ Операция отменена.")
        return ConversationHandler.END
        
    def run(self):
        """Запуск бота"""
        self.logger.info("Starting Client Insighting Bot...")
        self.application.run_polling()
        
    async def check_filters_periodic(self):
        """Периодическая проверка фильтров"""
        while True:
            try:
                with get_session() as db:
                    # Получаем всех активных пользователей
                    users = db.query(User).filter(User.is_active == True).all()
                    
                    for user in users:
                        # Получаем фильтры пользователя
                        filters = crud_user_filter.get_user_filters(user.id, db)
                        
                        for filter_item in filters:
                            try:
                                ebay_items = EbayItemFactory(filter_item.url)
                                new_items = crud_post.add_items_to_db(db=db, items=ebay_items.item_list)
                                
                                # Отправляем уведомления о новых объявлениях пользователю
                                for item in new_items:
                                    await self._send_item_notification_to_user(user, item)
                                    
                            except Exception as e:
                                self.logger.error(f"Error in periodic check for filter {filter_item.url}: {e}")
                                
            except Exception as e:
                self.logger.error(f"Error in periodic check: {e}")
                
            # Ждем 30 минут перед следующей проверкой
            await asyncio.sleep(1800)  # 30 минут
            
    async def _send_item_notification_to_user(self, user: User, item):
        """Отправка уведомления конкретному пользователю"""
        message = f"""
🆕 **Новое объявление!**

📌 **{item.title}**

💰 **Цена:** {item.price}
📍 **Местоположение:** {item.city}
📝 **Описание:** {item.description[:100]}{'...' if len(item.description) > 100 else ''}

🔗 [Открыть объявление]({item.link})
        """
        
        keyboard = [[InlineKeyboardButton("🔗 Открыть", url=item.link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        try:
            await self.application.bot.send_message(
                chat_id=user.telegram_id,
                text=message,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        except Exception as e:
            self.logger.error(f"Error sending notification to user {user.telegram_id}: {e}")
            
    async def _send_error_message(self, update: Update, message: str):
        """Отправка сообщения об ошибке"""
        if hasattr(update, 'callback_query'):
            await update.callback_query.edit_message_text(f"❌ {message}")
        else:
            await update.message.reply_text(f"❌ {message}")
            
    async def _send_item_notification_to_all_users(self, item):
        """Отправка уведомления всем пользователям"""
        # Здесь можно добавить логику для отправки всем подписчикам
        # Пока отправляем только в основной чат
        message = f"""
🆕 **Новое объявление!**

📌 **{item.title}**

💰 **Цена:** {item.price}
📍 **Местоположение:** {item.city}
📝 **Описание:** {item.description[:100]}{'...' if len(item.description) > 100 else ''}

🔗 [Открыть объявление]({item.link})
        """
        
        keyboard = [[InlineKeyboardButton("🔗 Открыть", url=item.link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Отправляем в основной чат (можно расширить для множественных пользователей)
        await self.application.bot.send_message(
            chat_id=settings.CHAT_ID,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        ) 