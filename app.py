# from typing import List, Optional

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


app = Flask(__name__)
app.register_blueprint(apidocs_views.blueprint, url_prefix="/api/docs")


@app.get("/api/baskets/")
@pydantic_api(name="Получить список корзин", tags=["Baskets"])
def get_baskets():
    return [
        Basket(
            id="",
            photo_url="",
            author_id="",
            name="",
            is_locked=False,
            created="",
            updated="",
        ).model_dump()
    ]


# /home/YakomazovPavel/projects/vaffelbot
# /home/YakomazovPavel/vaffelbot/app.py


# @app.get("/baskets/<int:basket_id>/dishes/")
# @pydantic_api(name="Получить список корзин", tags=["Baskets"])
# def get_baskets_dishes(id: str) -> List[BasketDish]:
#     pass


# @app.post("/baskets/<int:basket_id>/dishes/<int:dish_id>/")
# @pydantic_api(name="Получить список корзин", tags=["Baskets"])
# def create_baskets_dishes(
#     basket_id: str,
#     dish_id: str = ...,
#     body: BasketsBasketIdDishesDishIdPostRequest = None,
# ) -> BasketDish:
#     pass


# @app.delete(
#     "/baskets/{basket_id}/dishes/{dish_id}/", response_model=None, tags=["Baskets"]
# )
# def delete_baskets_dishes(basket_id: str, dish_id: str = ...) -> None:
#     pass


# @app.get("/categories/", response_model=List[Category], tags=["Categories"])
# def get_categories() -> List[Category]:
#     pass


# @app.get("/dishes/", response_model=List[Dish], tags=["Dishes"])
# def get_dishes(
#     category_id: Optional[str] = None, search: Optional[str] = None
# ) -> List[Dish]:
#     pass


# @app.post("/users/", response_model=User, tags=["Users"])
# def create_user(body: User = None) -> User:
#     pass


# @app.get("/users/{id}/", response_model=User, tags=["Users"])
# def get_user(id: str) -> User:
#     pass
