import logging

from flask import Flask, Response, request
from flask_pydantic_api import pydantic_api, apidocs_views


from models import (
    BasketModel,
    BasketDishModel,
    BasketsBasketIdDishesDishIdPostRequestModel,
    CategoryModel,
    DishModel,
    UserModel,
    CategoryListModel,
    BasketDishListModel,
    DishListModel,
    BasketListModel,
    GetBasketListRequestModel,
)

from type import CreateUserRequest, CreateBasketRequest

from storage import storage
from middleware import CustomWSGIMiddleware


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


app = Flask(__name__)
app.register_blueprint(apidocs_views.blueprint, url_prefix="/api/docs")
# app.before_request(authentication_middleware)

app.wsgi_app = CustomWSGIMiddleware(app.wsgi_app)


@app.get("/api/baskets/<int:id>")
@pydantic_api(name="Получить корзину", tags=["Baskets"])
def get_basket(id: int) -> BasketModel:
    # print(f"request.user {request.user}")
    basket = storage.get_basket_by_id(id=id)
    if basket:
        return BasketModel(
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


@app.get("/api/user/<int:user_id>/baskets/")
@pydantic_api(
    name="Получить список корзин",
    tags=["Baskets"],  # , merge_path_parameters=True
)
def get_baskets(user_id: int) -> BasketListModel:
    is_user = storage.check_user_id(id=user_id)
    if is_user:
        return storage.get_baskets(user_id=user_id)
    else:
        return Response(f"Пользователя {user_id} не найден", status=400)


@app.post("/api/baskets/")
@pydantic_api(name="Создать корзину", tags=["Baskets"])
def create_basket(body: CreateBasketRequest) -> BasketModel:
    is_user = storage.check_user_id(id=body.author_id)
    if is_user:
        basket = storage.create_basket(
            name=body.name,
            author_id=body.author_id
        )
        return basket
    else:
        return Response(f"Пользователя {body.author_id} не найден", status=400)


# /home/YakomazovPavel/projects/vaffelbot
# /home/YakomazovPavel/vaffelbot/app.py


# @app.get("/baskets/<int:basket_id>/dishes/")
# @pydantic_api(name="Получить список корзин", tags=["Baskets"])
# def get_baskets_dishes(id: str) -> List[BasketDish]:
#     pass


@app.get("/api/baskets/<int:basket_id>/dishes/")
@pydantic_api(
    name="Получить товары из корзины",
    tags=["BasketDish"],
)
def get_baskets_dishes(basket_id: int) -> BasketDishListModel:
    is_basket = storage.check_basket_id(id=basket_id)
    if is_basket:
        return storage.get_basket_dishes(basket_id=basket_id)
    else:
        return Response(f"Корзина {basket_id} не найдена", status=400)


@app.post("/api/baskets/<int:basket_id>/dishes/<int:dish_id>/")
@pydantic_api(
    name="Создать товар в корзине",
    tags=["BasketDish"],
)
def create_baskets_dishes(
    basket_id: int, dish_id: int, body: BasketsBasketIdDishesDishIdPostRequestModel
) -> BasketDishModel:
    basket = storage.get_basket_by_id(id=basket_id)
    dish = storage.get_dish_by_id(id=dish_id)
    user = storage.get_user_by_id(id=body.user_id)

    if basket and user and dish:
        return storage.create_basket_dish(
            basket_id=basket.id,
            user_id=user.id,
            dish_id=dish.id,
        )
    else:
        errors = []
        basket is None and errors.append(f"Корзина {basket_id} не найдена")
        user is None and errors.append(f"Польователь {body.user_id} не найден")
        dish is None and errors.append(f"Блюдо {dish_id} не найдено")
        message = ", ".join(errors)
        return Response(message, status=400)


# @app.delete(
#     "/baskets/{basket_id}/dishes/{dish_id}/", response_model=None, tags=["Baskets"]
# )
# def delete_baskets_dishes(basket_id: str, dish_id: str = ...) -> None:
#     pass


@app.get("/api/categories/")
@pydantic_api(name="Получить список категорий", tags=["Categories"])
def get_categories() -> CategoryListModel:
    return storage.get_categoryes()


@app.get("/api/dishes/")
@pydantic_api(name="Получить список блюд", tags=["Dishes"])
def get_dishes() -> DishListModel:
    return storage.get_dishes()


@app.post("/users/")
@pydantic_api(name="Создать пользователя", tags=["Users"])
def create_user(body: CreateUserRequest) -> UserModel:
    user = storage.get_telegram_user(body.telegram_id)
    if not user:
        user = storage.create_user(
            telegram_id=body.telegram_id,
            username=body.username,
            first_name=body.first_name,
            last_name=body.last_name,
            photo_url=body.photo_url,
        )

    return user


# @app.get("/users/{id}/", response_model=User, tags=["Users"])
# def get_user(id: str) -> User:
#     pass
