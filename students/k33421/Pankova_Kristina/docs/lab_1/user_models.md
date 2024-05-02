## Пользовательские модели

```python
class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str
    budgets: List["Budget"] = Relationship(back_populates="user")
    transactions: List["FinancialTransaction"] = Relationship(back_populates="user")
```

Модель User представляет пользователя системы. Она имеет следующие атрибуты:

- id (int): Идентификатор пользователя (первичный ключ).
- name (str): Имя пользователя.
- email (str): Адрес электронной почты пользователя.
- password (str): Пароль пользователя.
- budgets (List["Budget"]): Список бюджетов, принадлежащих пользователю (связь один-ко-многим с моделью Budget).
- transactions (List["FinancialTransaction"]): Список финансовых транзакций, совершенных пользователем (связь один-ко-многим с моделью FinancialTransaction).

## Модель UserInput

```python
class UserInput(SQLModel):
    name: str
    password: str = Field(max_length=256, min_length=6)
    password2: str
    email: EmailStr = Field(sa_column=Column(String, index=True, unique=True))
    is_seller: bool = False

    @field_validator('password2')
    def password_match(cls, v, values, **kwargs):
        print(values)
        if v != values.data['password']:
            raise ValueError('passwords don\'t match')
        return v
```

Модель UserInput используется для ввода данных при регистрации нового пользователя. Она имеет следующие атрибуты:

- name (str): Имя пользователя.
- password (str): Пароль пользователя (длина должна быть от 6 до 256 символов).
- password2 (str): Поле для подтверждения пароля.
- email (EmailStr): Адрес электронной почты пользователя (должен быть уникальным и индексируемым в базе данных).
- is_seller (bool): Флаг, указывающий, является ли пользователь продавцом (по умолчанию False).

Кроме того, модель имеет валидатор password_match, который проверяет, что значения полей password и password2 совпадают.

## Модель UserLogin

```python
class UserLogin(SQLModel):
    name: str
    password: str
```

Модель UserLogin используется для ввода данных при аутентификации пользователя. Она имеет следующие атрибуты:

- name (str): Имя пользователя.
- password (str): Пароль пользователя.