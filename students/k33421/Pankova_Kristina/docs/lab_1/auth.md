# Документация для auth.py

Файл auth.py содержит класс AuthHandler, который реализует функциональность аутентификации и авторизации пользователей с использованием JSON Web Tokens (JWT).

## Класс AuthHandler
```python
class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'])
    secret = 'supersecret'
```
Класс AuthHandler имеет следующие атрибуты:

- security: Экземпляр HTTPBearer для обработки заголовка Authorization в входящих запросах.
- pwd_context: Экземпляр CryptContext для хэширования и верификации паролей с использованием алгоритма bcrypt.
- secret: Секретный ключ для шифрования и дешифрования JWT-токенов.

### Методы

#### get_password_hash(self, password)
```python
def get_password_hash(self, password):
    return self.pwd_context.hash(password)
```
Этот метод принимает пароль в виде строки и возвращает его хэшированное значение с использованием алгоритма bcrypt.

#### verify_password(self, pwd, hashed_pwd)
```python
def verify_password(self, pwd, hashed_pwd):
    return self.pwd_context.verify(pwd, hashed_pwd)
```
Этот метод проверяет, совпадает ли введенный пароль (pwd) с хэшированным паролем (hashed_pwd). Возвращает True, если пароли совпадают, и False в противном случае.

#### encode_token(self, user_id)
```python
def encode_token(self, user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, self.secret, algorithm='HS256')
```
Этот метод генерирует JWT-токен для указанного user_id. Токен содержит следующие поля:

- exp (expiration time): Время истечения срока действия токена (через 8 часов после создания).
- iat (issued at): Время создания токена.
- sub (subject): Идентификатор пользователя.

Токен шифруется с использованием секретного ключа и алгоритма HS256.

#### decode_token(self, token)
```python
def decode_token(self, token):
    try:
        payload = jwt.decode(token, self.secret, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Expired signature')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')
```
Этот метод дешифрует JWT-токен и извлекает идентификатор пользователя (sub). Если срок действия токена истек (ExpiredSignatureError), возвращается ошибка 401 Unauthorized с соответствующим сообщением. Если токен недействителен (InvalidTokenError), также возвращается ошибка 401 Unauthorized.

#### auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security))
```python
def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
    return self.decode_token(auth.credentials)
```
Этот метод является обёрткой для decode_token, которая принимает HTTPAuthorizationCredentials из заголовка Authorization входящего запроса.

#### get_current_user(self, auth: HTTPAuthorizationCredentials = Security(security))
```python
def get_current_user(self, auth: HTTPAuthorizationCredentials = Security(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials'
    )
    username = self.decode_token(auth.credentials)
    if username is None:
        raise credentials_exception
    user = find_user(username)
    if user is None:
        raise credentials_exception
    return user
```
