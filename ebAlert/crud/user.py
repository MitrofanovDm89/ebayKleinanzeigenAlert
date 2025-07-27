from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ebAlert.crud.base import CRUDBase
from ebAlert.models.user_models import User, UserFilter
from ebAlert.db.db import get_session

class CRUDUser(CRUDBase[User]):
    """CRUD операции для пользователей"""
    
    def get_by_telegram_id(self, telegram_id: int, db: Session) -> Optional[User]:
        """Получить пользователя по Telegram ID"""
        return db.query(User).filter(User.telegram_id == telegram_id).first()
    
    def create_or_get_user(self, telegram_id: int, username: str = None, 
                          first_name: str = None, last_name: str = None, 
                          db: Session = None) -> User:
        """Создать или получить пользователя"""
        if db is None:
            with get_session() as db:
                return self._create_or_get_user_internal(telegram_id, username, first_name, last_name, db)
        else:
            return self._create_or_get_user_internal(telegram_id, username, first_name, last_name, db)
    
    def _create_or_get_user_internal(self, telegram_id: int, username: str = None,
                                   first_name: str = None, last_name: str = None,
                                   db: Session = None) -> User:
        """Внутренний метод для создания или получения пользователя"""
        user = self.get_by_telegram_id(telegram_id, db)
        
        if user is None:
            # Создаем нового пользователя
            user_data = {
                "telegram_id": telegram_id,
                "username": username,
                "first_name": first_name,
                "last_name": last_name
            }
            user = self.create(user_data, db)
        else:
            # Обновляем информацию о пользователе
            if username:
                user.username = username
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            db.commit()
            db.refresh(user)
            
        return user

class CRUDUserFilter(CRUDBase[UserFilter]):
    """CRUD операции для фильтров пользователей"""
    
    def get_user_filters(self, user_id: int, db: Session) -> List[UserFilter]:
        """Получить все фильтры пользователя"""
        return db.query(UserFilter).filter(
            and_(UserFilter.user_id == user_id, UserFilter.is_active == True)
        ).all()
    
    def get_by_url_and_user(self, url: str, user_id: int, db: Session) -> Optional[UserFilter]:
        """Получить фильтр по URL и пользователю"""
        return db.query(UserFilter).filter(
            and_(
                UserFilter.url == url,
                UserFilter.user_id == user_id,
                UserFilter.is_active == True
            )
        ).first()
    
    def create_user_filter(self, user_id: int, url: str, name: str = None, db: Session = None) -> UserFilter:
        """Создать фильтр для пользователя"""
        if db is None:
            with get_session() as db:
                return self._create_user_filter_internal(user_id, url, name, db)
        else:
            return self._create_user_filter_internal(user_id, url, name, db)
    
    def _create_user_filter_internal(self, user_id: int, url: str, name: str = None, db: Session = None) -> UserFilter:
        """Внутренний метод для создания фильтра"""
        filter_data = {
            "user_id": user_id,
            "url": url,
            "name": name
        }
        return self.create(filter_data, db)
    
    def deactivate_filter(self, filter_id: int, user_id: int, db: Session) -> bool:
        """Деактивировать фильтр пользователя"""
        filter_obj = db.query(UserFilter).filter(
            and_(UserFilter.id == filter_id, UserFilter.user_id == user_id)
        ).first()
        
        if filter_obj:
            filter_obj.is_active = False
            db.commit()
            return True
        return False

# Создаем экземпляры CRUD классов
crud_user = CRUDUser(User)
crud_user_filter = CRUDUserFilter(UserFilter) 