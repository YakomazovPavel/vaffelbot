from typing import List, Optional
import logging

from flask import Flask
from flask_pydantic_api import pydantic_api, apidocs_views


from models import (
    Basket,
    BasketDish,
    BasketsBasketIdDishesDishIdPostRequest,
    Category,
    Dish,
    User,
)

from database import storage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


app = Flask(__name__)
app.register_blueprint(apidocs_views.blueprint, url_prefix="/api/docs")


# @app.get("/api/baskets/")
# @pydantic_api(name="Получить список корзин", tags=["Baskets"])
# def get_baskets():
#     return [
#         Basket(
#             id="",
#             photo_url="",
#             author_id="",
#             name="",
#             is_locked=False,
#             created="",
#             updated="",
#         ).model_dump()
#     ]


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
    # print("dishes", dishes)
    # print("dishes", dishes[0][1])
    # print("dishes id", getattr(dishes[0][0], "id", "id"))
    # print("dishes category_id", getattr(dishes[0][1], "category_id", "category_id"))
    # return "get_dishes"
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


# @app.post("/users/", response_model=User, tags=["Users"])
# def create_user(body: User = None) -> User:
#     pass


# @app.get("/users/{id}/", response_model=User, tags=["Users"])
# def get_user(id: str) -> User:
#     pass
