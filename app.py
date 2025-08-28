from typing import List, Optional
import logging

from flask import Flask, Response
from flask_pydantic_api import pydantic_api, apidocs_views


from models import (
    Basket,
    BasketDish,
    BasketsBasketIdDishesDishIdPostRequest,
    Category,
    Dish,
    User,
)

from type import CreateUserRequest, CreateBasketRequest

from database import storage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


app = Flask(__name__)
app.register_blueprint(apidocs_views.blueprint, url_prefix="/api/docs")


@app.get("/api/baskets/<int:id>")
@pydantic_api(name="Получить корзину", tags=["Baskets"])
def get_basket(id: int):
    basket = storage.get_basket_by_id(id=id)
    if basket:
        return Basket(
            id=basket.id,
            photo_url=basket.photo_url,
            author_id=basket.author_id,
            name=basket.name,
            is_locked=basket.is_locked,
            created=basket.created,
            updated=basket.updated,
        )
    else:
        return Response(status=404)


@app.get("/api/baskets/")
@pydantic_api(name="Получить список корзин", tags=["Baskets"])
def get_baskets():
    categoryes = storage.get_baskets()
    return [
        Basket(
            id=basket.id,
            photo_url=basket.photo_url,
            author_id=basket.author_id,
            name=basket.name,
            is_locked=basket.is_locked,
            created=basket.created,
            updated=basket.updated,
        ).model_dump()
        for basket in categoryes
    ]


@app.post("/api/baskets/")
@pydantic_api(name="Создать корзину", tags=["Baskets"])
def create_basket(body: CreateBasketRequest) -> Basket:
    user = storage.get_user_by_id(id=body.author_id)
    if user:
        basket = storage.create_basket(
            name=body.name,
            author_id=body.author_id,
            photo_url=body.photo_url,
        )
        return Basket(
            id=basket.id,
            photo_url=basket.photo_url,
            author_id=basket.author_id,
            name=basket.name,
            is_locked=basket.is_locked,
            created=basket.created,
            updated=basket.updated,
        )
    else:
        return Response(f"Пользователя с id={body.author_id} не существует", status=400)


# /home/YakomazovPavel/projects/vaffelbot
# /home/YakomazovPavel/vaffelbot/app.py


# @app.get("/baskets/<int:basket_id>/dishes/")
# @pydantic_api(name="Получить список корзин", tags=["Baskets"])
# def get_baskets_dishes(id: str) -> List[BasketDish]:
#     pass


# @app.post("/api/baskets/<int:basket_id>/dishes/<int:dish_id>/")
# @pydantic_api(
#     name="Создать товар в корзине",
#     tags=["BasketDish"],
#     merge_path_parameters=True,
# )
# def create_baskets_dishes(data: BasketsBasketIdDishesDishIdPostRequest) -> BasketDish:
#     return f"basket_id {data.basket_id} dish_id {data.dish_id} user_id {data.user_id}"


# @app.delete(
#     "/baskets/{basket_id}/dishes/{dish_id}/", response_model=None, tags=["Baskets"]
# )
# def delete_baskets_dishes(basket_id: str, dish_id: str = ...) -> None:
#     pass


@app.get("/api/categories/")
@pydantic_api(name="Получить список категорий", tags=["Categories"])
def get_categories() -> List[Category]:
    categoryes = storage.get_categoryes()
    return [Category(id=item.id, name=item.name).model_dump() for item in categoryes]


@app.get("/api/dishes/")
@pydantic_api(name="Получить список блюд", tags=["Dishes"])
def get_dishes() -> List[Dish]:
    dishes = storage.get_dishes()
    return [
        Dish(
            id=dish.id,
            category_id=category,
            name=dish.name,
            description=dish.description,
            price=dish.price,
            calories=dish.calories,
            proteins=dish.proteins,
            fats=dish.fats,
            carbs=dish.carbs,
            weight=dish.weight,
            photo_url=dish.photo_url,
        ).model_dump()
        for dish, category in dishes
    ]


@app.post("/users/")
@pydantic_api(name="Создать пользователя", tags=["Users"])
def create_user(body: CreateUserRequest) -> User:
    user = storage.get_telegram_user(body.telegram_id)
    if not user:
        user = storage.create_user(
            telegram_id=body.telegram_id,
            username=body.username,
            first_name=body.first_name,
            last_name=body.last_name,
            photo_url=body.photo_url,
        )

    return User(
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        photo_url=user.photo_url,
        telegram_id=user.telegram_id,
    )


# @app.get("/users/{id}/", response_model=User, tags=["Users"])
# def get_user(id: str) -> User:
#     pass
