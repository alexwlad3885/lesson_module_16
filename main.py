
"""Домашнее задание по теме 'Основы Fast Api и маршрутизация'"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/module_16_1")
async def welcome() -> dict:
    return {"message": "Главная страница"}