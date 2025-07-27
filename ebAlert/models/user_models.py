from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ebAlert.db.db import Base, engine

class User(Base):
    """Модель пользователя Telegram"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Связь с фильтрами пользователя
    filters = relationship("UserFilter", back_populates="user", cascade="all, delete-orphan")

class UserFilter(Base):
    """Модель фильтра пользователя"""
    __tablename__ = "user_filters"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=True)  # Название фильтра (опционально)
    url = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связь с пользователем
    user = relationship("User", back_populates="filters")

# Создаем таблицы
Base.metadata.create_all(engine) 