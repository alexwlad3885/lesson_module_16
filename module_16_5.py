"""Домашнее задание по теме 'Шаблонизатор Jinja 2'"""
from fastapi import FastAPI, status, Body, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")
users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/")
def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/users/{user_id}")
def get_users(request: Request, user_id: int) -> HTMLResponse:
    try:
        index_user = [i for i in range(len(users)) if (users[i]['id'] == user_id)][0]
        return templates.TemplateResponse("users.html", {"request": request, "user": users[index_user]})
    except IndexError:
        raise HTTPException(status_code=404, detail='User not found')


@app.post('/users/{username}/{age}')
def create_user(username: str, age: int) -> User:
    if len(users) == 0:
        user_id = 1
    else:
        user_id = users[-1]['id'] + 1
    user = User(id=user_id, username=username, age=age)
    users.append({'id': user.id, 'username': user.username, 'age': user.age})
    return user


@app.put('/user/{user_id}/{username}/{age}')
def update_user(user_id: int, username: str, age: int) -> dict:
    try:
        edit_user = users[user_id - 1]
        edit_user['username'] = username
        edit_user['age'] = age
        return edit_user
    except IndexError:
        raise HTTPException(status_code=404, detail='User not found')


@app.delete('/user/{user_id}')
def delite_user(user_id: int) -> dict:
    try:
        delete_user = users.pop([i for i in range(len(users)) if (users[i]['id'] == user_id)][0])
        return delete_user
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')

