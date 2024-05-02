# Финансовые модели

## Модель Budget

Модель Budget представляет бюджет пользователя. Бюджет имеет следующие атрибуты:

- id (Optional[int]): Идентификатор бюджета (первичный ключ).
- name (str): Название бюджета.
- amount (float): Общая сумма бюджета.
- user_id (Optional[int]): Идентификатор пользователя, которому принадлежит бюджет (внешний ключ).
- user (Optional[User]): Связь один-к-одному с моделью User.
- categories (List["BudgetCategory"]): Список категорий бюджета (связь многие-ко-многим с моделью Category).

```python
class Budget(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    amount: float
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="budgets", sa_relationship_kwargs={"cascade": "delete"})
    categories: List["BudgetCategory"] = Relationship(back_populates="budget", sa_relationship_kwargs={"cascade": "delete"})
```

## Модель BudgetCategory

Модель BudgetCategory представляет связующую таблицу между бюджетами и категориями. Она имеет следующие атрибуты:

- id (Optional[int]): Идентификатор связи (первичный ключ).
- budget_id (Optional[int]): Идентификатор бюджета (внешний ключ).
- category_id (Optional[int]): Идентификатор категории (внешний ключ).
- budget (Optional[Budget]): Связь один-к-одному с моделью Budget.
- category (Optional["Category"]): Связь один-к-одному с моделью Category.
- budget_amount (float): Сумма, выделенная для данной категории в рамках бюджета.

```python
class BudgetCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    budget_id: Optional[int] = Field(default=None, foreign_key="budget.id")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    budget: Optional[Budget] = Relationship(back_populates="categories", sa_relationship_kwargs={"cascade": "delete"})
    category: Optional["Category"] = Relationship(back_populates="budgets", sa_relationship_kwargs={"cascade": "delete"})
    budget_amount: float
```

## Модель Category

Модель Category представляет категорию расходов. Она имеет следующие атрибуты:

- id (Optional[int]): Идентификатор категории (первичный ключ).
- name (str): Название категории.
- budgets (List[BudgetCategory]): Список бюджетов, в которые входит данная категория (связь многие-ко-многим с моделью Budget).
- transactions (List["FinancialTransaction"]): Список финансовых транзакций, относящихся к данной категории (связь один-ко-многим с моделью FinancialTransaction).

```python
class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    budgets: List[BudgetCategory] = Relationship(back_populates="category", sa_relationship_kwargs={"cascade": "delete"})
    transactions: List["FinancialTransaction"] = Relationship(back_populates="category", sa_relationship_kwargs={"cascade": "delete"})
```


## Модель FinancialTransaction

Модель FinancialTransaction представляет финансовую транзакцию (расход или доход). Она имеет следующие атрибуты:

- id (Optional[int]): Идентификатор транзакции (первичный ключ).
- description (str): Описание транзакции.
- amount (float): Сумма транзакции.
- date (datetime): Дата транзакции.
- user_id (Optional[int]): Идентификатор пользователя, совершившего транзакцию (внешний ключ).
- category_id (Optional[int]): Идентификатор категории, к которой относится данная транзакция (внешний ключ).
- user (Optional[User]): Связь один-к-одному с моделью User.
- category (Optional[Category]): Связь один-к-одному с моделью Category.

```python
class FinancialTransaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    amount: float
    date: datetime
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    user: Optional[User] = Relationship(back_populates="transactions", sa_relationship_kwargs={"cascade": "delete"})
    category: Optional[Category] = Relationship(back_populates="transactions", sa_relationship_kwargs={"cascade": "delete"})
```


## Модель Goal

Модель Goal представляет финансовую цель пользователя. Она имеет следующие атрибуты:

- id (int): Идентификатор цели (первичный ключ).
- description (str): Описание цели.
- target_amount (float): Целевая сумма для достижения цели.
- user_id (int): Идентификатор пользователя, которому принадлежит цель.


```python
class Goal(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    description: str
    target_amount: float
    user_id: int
```

