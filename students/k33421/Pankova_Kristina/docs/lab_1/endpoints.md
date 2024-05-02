# Документация эндпойнтов

## Эндпойнты бюджетов

### GET /budgets

```python
@finance_router.get("/budgets")
def get_budgets(session: Session = Depends(get_session)):
    budgets = session.exec(select(Budget)).all()
    return budgets
```
Этот эндпойнт возвращает список всех бюджетов.

### GET /budgets/{budget_id}

```python
@finance_router.get("/budgets/{budget_id}", response_model=dict)
def get_budget_details(budget_id: int, session: Session = Depends(get_session)):
    budget = session.get(Budget, budget_id)
    if not budget:
        return {"message": "Budget not found"}
    user = budget.user
    budget_categories = session.exec(
        select(BudgetCategory).where(BudgetCategory.budget_id == budget_id)
    ).all()
    caterogies = []
    for bud in budget_categories:
        category_id = bud.category_id
        caterogies.append(session.exec(select(Category).where(Category.id == category_id)).first().dict())
    budget_data = budget.dict()
    user_data = user.dict() if user else None
    budget_data["user"] = user_data
    budget_data["categories"] = caterogies
    return budget_data
```
Этот эндпойнт возвращает подробную информацию о бюджете с указанным budget_id, включая связанные данные о пользователе и категориях.

### POST /budget

```python
@finance_router.post("/budget")
def create_budget(budget: Budget, session: Session = Depends(get_session)):
    session.add(budget)
    session.commit()
    session.refresh(budget)
    return budget
```
Этот эндпойнт позволяет создать новый бюджет.

## Эндпойнты связующей таблицы BudgetCategory

### GET /budget_categories

```python
@finance_router.get("/budget_categories")
def get_budget_categories(session: Session = Depends(get_session)):
    budget_categories = session.exec(select(BudgetCategory)).all()
    return budget_categories
```
Этот эндпойнт возвращает список всех записей в связующей таблице BudgetCategory.

### GET /budget_category/{budget_category_id}

```python
@finance_router.get("/budget_category/{budget_category_id}")
def get_budget_category(budget_category_id: int, session: Session = Depends(get_session)):
    try:
        budget_category = session.get(BudgetCategory, budget_category_id)
        return budget_category
    except NoResultFound:
        return {"message": "Budget Category not found"}
```
Этот эндпойнт возвращает запись в связующей таблице BudgetCategory с указанным budget_category_id.

### POST /budget_category

```python
@finance_router.post("/budget_category")
def create_budget_category(budget_category: BudgetCategory, session: Session = Depends(get_session)):
    session.add(budget_category)
    session.commit()
    session.refresh(budget_category)
    return budget_category
```
Этот эндпойнт позволяет создать новую запись в связующей таблице BudgetCategory.

## Эндпойнты категорий

### GET /categories

```python
@finance_router.get("/categories")
def get_categories(session: Session = Depends(get_session)):
    categories = session.exec(select(Category)).all()
    return categories
```
Этот эндпойнт возвращает список всех категорий.

### GET /category/{category_id}

```python
@finance_router.get("/category/{category_id}")
def get_category(category_id: int, session: Session = Depends(get_session)):
    try:
        category = session.get(Category, category_id)
        return category
    except NoResultFound:
        return {"message": "Category not found"}
```
Этот эндпойнт возвращает категорию с указанным category_id.

### POST /category

```python
@finance_router.post("/category")
def create_category(category: Category, session: Session = Depends(get_session)):
    session.add(category)
```

# Документация для эндпойнтов пользователя

## Регистрация пользователя

### POST /registration

```python
@user_router.post('/registration', status_code=201, tags=['users'],
                  description='Register new user')
def register(user: UserInput, session: Session = Depends(get_session)):
    users = select_all_users()
    if any(x.name == user.name for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_pwd = auth_handler.get_password_hash(user.password)
    u = User(name=user.name, password=hashed_pwd, email=user.email)
    session.add(u)
    session.commit()
    return JSONResponse(status_code=HTTP_201_CREATED, content='OK')
```
Этот эндпойнт позволяет зарегистрировать нового пользователя в системе. Он принимает объект UserInput, содержащий имя пользователя, электронную почту, пароль и подтверждение пароля.

Если имя пользователя уже занято, возвращается ошибка 400 Bad Request с соответствующим сообщением. В противном случае пароль хэшируется, создается новый объект User и сохраняется в базе данных. После успешной регистрации возвращается ответ 201 Created с сообщением "OK".

## Аутентификация пользователя

### POST /login

```python
@user_router.post('/login', tags=['users'])
def login(user: UserLogin):
    user_found = find_user(user.name)
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user_found.name)
    return {'token': token}
```
Этот эндпойнт используется для аутентификации пользователя. Он принимает объект UserLogin, содержащий имя пользователя и пароль.

Если пользователь с указанным именем не найден или введенный пароль не совпадает с сохраненным паролем, возвращается ошибка 401 Unauthorized с соответствующим сообщением. В случае успешной аутентификации генерируется JWT-токен с помощью функции auth_handler.encode_token() и возвращается в ответе.

## Получение текущего пользователя

### GET /users/me

```python
@user_router.get('/users/me', tags=['users'])
def get_current_user(user: User = Depends(auth_handler.get_current_user)):
    return user
```
Этот эндпойнт возвращает информацию о текущем аутентифицированном пользователе. Он использует зависимость auth_handler.get_current_user, которая извлекает пользователя из JWT-токена, передаваемого в заголовке Authorization.

## Изменение пароля

### PUT /change_password

```python
@user_router.put('/change_password', tags=['users'])
def change_password(new_password: str, current_user: User = Depends(auth_handler.get_current_user), session: Session = Depends(get_session)):
    if not auth_handler.verify_password(new_password.password, current_user.password):
        raise HTTPException(status_code=400, detail='Invalid current password')
    hashed_new_password = auth_handler.get_password_hash(new_password)
    current_user.password = hashed_new_password
    session.commit()
    return {'message': 'Password changed successfully'}
```
Этот эндпойнт позволяет аутентифицированному пользователю изменить свой пароль. Он принимает новый пароль в теле запроса.
