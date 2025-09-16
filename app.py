import asyncio
import logging
import uuid

from flask import Flask, Response, request
from flask_pydantic_api import pydantic_api, apidocs_views


from models import (
    BasketModel,
    BasketDishModel,
    BasketsBasketIdDishesDishIdPostRequestModel,
    UserModel,
    CategoryListModel,
    BasketDishListModel,
    DishListModel,
    BasketListModel,
    PrepareMessage,
)
from aiogram.types import (
    InlineQueryResultPhoto,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from flask_cors import CORS, cross_origin

from type import CreateUserRequest, CreateBasketRequest

from storage import storage
from middleware import AuthenticationMiddleware
from database import Basket
import traceback

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


app = Flask(__name__)
app.before_request(AuthenticationMiddleware)
app.register_blueprint(apidocs_views.blueprint, url_prefix="/api/docs")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


# app.wsgi_app = CustomWSGIMiddleware(app.wsgi_app)


@app.get("/api/baskets/<int:id>/")
@cross_origin()
@pydantic_api(name="Получить корзину", tags=["Baskets"])
def get_basket(id: int) -> BasketModel:
    basket = storage.get_basket_by_id(id=id)
    if basket:
        print(f"request.user {request.user}")
        if request.user:
            if not storage.check_basket_user(
                user_id=request.user.id,
                basket_id=basket.id,
            ):
                storage.create_basket_user(user_id=request.user.id, basket_id=basket.id)

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


async def create_prepare_message(
    telegram_id: int,
):  # basket: Basket, telegram_id: int, id: str
    from bot import bot

    try:
        message = await bot.bot.save_prepared_inline_message(
            user_id=telegram_id,
            result=InlineQueryResultPhoto(
                id=str(uuid.uuid4()),
                # photo_url=basket.photo_url,
                # thumbnail_url=basket.photo_url,
                photo_url="https://raw.githubusercontent.com/YakomazovPavel/YakomazovPavel.github.io/main/public/assets/2.jpg",
                thumbnail_url="https://raw.githubusercontent.com/YakomazovPavel/YakomazovPavel.github.io/main/public/assets/2.jpg",
                title="basket.name",
                description="Description",
                caption="Добавляйте свои вафли в совместную корзину ",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="Добавить",
                                url="https://t.me/vaffel2_bot/vaffel?startapp=1",
                            )
                        ]
                    ]
                ),
            ),
            #
            allow_bot_chats=True,
            allow_channel_chats=True,
            allow_group_chats=True,
            allow_user_chats=True,
        )
        print(f"message {message}")

        return message
    except Exception as e:
        print(f"!ERROR {e}")
        traceback.print_exc()


@app.get("/api/baskets/<int:id>/share/")
@cross_origin()
@pydantic_api(name="Поделиться корзиной", tags=["Baskets"])
def share_basket(id: int) -> PrepareMessage:
    basket = storage.get_basket_by_id(id=id)
    if basket:
        print(f"telegram_id {request.user}")
        res_message = asyncio.get_event_loop().run_until_complete(
            create_prepare_message(
                # basket=basket,
                telegram_id=request.user.telegram_id,
                # id=str(uuid.uuid4()),
            )
        )
        return PrepareMessage(id=res_message.id)
    else:
        return Response(status=400)


@app.get("/api/user/<int:user_id>/baskets/")
@cross_origin()
@pydantic_api(
    name="Получить список корзин",
    tags=["Baskets"],  # , merge_path_parameters=True
)
def get_baskets(user_id: int) -> BasketListModel:
    print(f"!user {request.user}")
    is_user = storage.check_user_id(id=user_id)
    if is_user:
        return storage.get_baskets(user_id=user_id)
    else:
        return Response(f"Пользователя {user_id} не найден", status=400)


@app.post("/api/baskets/")
@cross_origin()
@pydantic_api(name="Создать корзину", tags=["Baskets"])
def create_basket(body: CreateBasketRequest) -> BasketModel:
    is_user = storage.check_user_id(id=body.author_id)
    if is_user:
        basket = storage.create_basket(name=body.name, author_id=body.author_id)
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
@cross_origin()
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
@cross_origin()
@pydantic_api(name="Создать товар в корзине", tags=["BasketDish"])
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


@app.delete("/api/baskets/<int:basket_id>/dishes/<int:dish_id>/")
@cross_origin()
@pydantic_api(name="Удалить товар из корзины", tags=["BasketDish"])
def delete_baskets_dishes(basket_id: int, dish_id: int) -> BasketDishModel:
    print(f"!user {request.user}")
    basket = storage.get_basket_by_id(id=basket_id)
    dish = storage.get_dish_by_id(id=dish_id)

    if not basket or not dish:
        errors = []
        basket is None and errors.append(f"Корзина {basket_id} не найдена")
        dish is None and errors.append(f"Блюдо {dish_id} не найдено")
        message = ", ".join(errors)
        return Response(message, status=400)
    else:
        basket_dish = storage.remove_basket_dish(basket_id=basket.id, dish_id=dish.id)
        return basket_dish or Response(
            f"Не удалось удалить блюдо {dish_id} из корзины {basket_id}", status=500
        )


@app.get("/api/categories/")
@cross_origin()
@pydantic_api(name="Получить список категорий", tags=["Categories"])
def get_categories() -> CategoryListModel:
    return storage.get_categoryes()


@app.get("/api/dishes/")
@cross_origin()
@pydantic_api(name="Получить список блюд", tags=["Dishes"])
def get_dishes() -> DishListModel:
    return storage.get_dishes()


@app.post("/api/users/")
@cross_origin()
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
