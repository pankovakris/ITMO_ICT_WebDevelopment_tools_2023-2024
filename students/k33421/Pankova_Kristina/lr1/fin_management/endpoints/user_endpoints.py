from fastapi import APIRouter, HTTPException, Security, security, Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED,HTTP_404_NOT_FOUND

from authentification.auth import AuthHandler
from db.connection import *
from models.user_models import UserInput, User, UserLogin
from repos.user_repos import select_all_users, find_user

user_router = APIRouter()
auth_handler = AuthHandler()


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


@user_router.get('/users/me', tags=['users'])
def get_current_user(user: User = Depends(auth_handler.get_current_user)):
    return user

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


@user_router.put('/change_password', tags=['users'])
def change_password(new_password: str, token: str = None, session: Session = Depends(get_session)):
    try:
        username = auth_handler.decode_token(token)
        user = find_user(username)
        if user is None:
            raise HTTPException(status_code=401, detail='Invalid token')

        hashed_new_password = auth_handler.get_password_hash(new_password)
        updated_user = User(name=user.name, password=hashed_new_password, email=user.email)
        session.merge(updated_user)
        session.commit()

        return {'message': 'Password changed successfully'}
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid token or password change failed')
