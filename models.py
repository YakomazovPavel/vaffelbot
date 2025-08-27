from typing import Optional

from pydantic import BaseModel, Field


class Category(BaseModel):
    id: Optional[int] = Field(None, example=1)
    name: Optional[str] = Field(None, example="Сырные вафли")


class Dish(BaseModel):
    id: Optional[int] = None
    category_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[float] = None
    proteins: Optional[float] = None
    fats: Optional[float] = None
    carbs: Optional[float] = None
    weight: Optional[float] = None
    photo_url: Optional[str] = None


class User(BaseModel):
    id: Optional[int] = Field(None, example="123123")
    username: Optional[str] = Field(None, example="@pavel")
    first_name: Optional[str] = Field(None, example="pavel")
    last_name: Optional[str] = Field(None, example="durov")
    photo_url: Optional[str] = Field(
        None,
        example="https://pic.rutube.ru/video/fa/17/fa1763b889c5e26146174f8878315143.jpg",
    )
    telegram_id: str


class Basket(BaseModel):
    id: Optional[str] = None
    photo_url: Optional[str] = None
    author_id: Optional[str] = None
    name: Optional[str] = None
    is_locked: Optional[bool] = None
    created: Optional[str] = None
    updated: Optional[str] = None


class BasketDish(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[float] = None
    proteins: Optional[float] = None
    fats: Optional[float] = None
    carbs: Optional[float] = None
    weight: Optional[float] = None
    photo_url: Optional[str] = None
    user_id: Optional[str] = None


class BasketsBasketIdDishesDishIdPostRequest(BaseModel):
    user_id: Optional[str] = None
    dish_id: Optional[str] = None
    basket_id: Optional[str] = None
