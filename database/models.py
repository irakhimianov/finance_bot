from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (Column, String, Integer,
                        BigInteger, Float, Boolean,
                        DateTime, ForeignKey, select)

from database import Base


class User(Base):
    __tablename__ = 'user'

    telegram_id = Column(BigInteger, primary_key=True, nullable=False)
    city = Column(String)

    def __repr__(self):
        return f'<User> {self.id} - {self.telegram_id} - {self.city}'


class Category(Base):
    __tablename__ = 'category'

    codename = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    aliases = Column(String)
    expense = relationship('Expense', backref='expense', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Category> {self.codename} - {self.name} - {self.aliases}'


class Expense(Base):
    __tablename__ = 'expense'

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    category_codename = Column(String, ForeignKey('category.codename'), nullable=False)

    def __repr__(self):
        return f'<Expense> {self.id} - {self.amount:.2f} - {self.created_at.strftime("%d.%m.%Y %H:%M")} - ' \
               f'{self.category_codename}'
