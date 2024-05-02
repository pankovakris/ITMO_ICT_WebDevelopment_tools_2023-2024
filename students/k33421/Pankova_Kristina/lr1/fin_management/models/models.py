from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from .user_models import *
from datetime import datetime

from .user_models import User


class Budget(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    amount: float
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="budgets", sa_relationship_kwargs={"cascade": "delete"})
    categories: List["BudgetCategory"] = Relationship(back_populates="budget", sa_relationship_kwargs={"cascade": "delete"})

# Связующая таблица между бюджетами и категориями
class BudgetCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    budget_id: Optional[int] = Field(default=None, foreign_key="budget.id")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    budget: Optional[Budget] = Relationship(back_populates="categories", sa_relationship_kwargs={"cascade": "delete"})
    category: Optional["Category"] = Relationship(back_populates="budgets", sa_relationship_kwargs={"cascade": "delete"})
    budget_amount: float  # Поле, характеризующее связь

# Таблица категорий
class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    budgets: List[BudgetCategory] = Relationship(back_populates="category", sa_relationship_kwargs={"cascade": "delete"})
    transactions: List["FinancialTransaction"] = Relationship(back_populates="category", sa_relationship_kwargs={"cascade": "delete"})

# Таблица финансовых транзакций
class FinancialTransaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    amount: float
    date: datetime
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    user: Optional[User] = Relationship(back_populates="transactions", sa_relationship_kwargs={"cascade": "delete"})
    category: Optional[Category] = Relationship(back_populates="transactions", sa_relationship_kwargs={"cascade": "delete"})

class Goal(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    description: str
    target_amount: float
    user_id: int

