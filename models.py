from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, Field, field_serializer, RootModel


class CategoryModel(BaseModel):
    id: Optional[int] = Field(None, example=1)
    name: Optional[str] = Field(None, example="Сырные вафли")


class DishModel(BaseModel):
    id: Optional[int] = None
    category: CategoryModel | None = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[float] = None
    proteins: Optional[float] = None
    fats: Optional[float] = None
    carbs: Optional[float] = None
    weight: Optional[float] = None
    photo_url: Optional[str] = None
    color: Optional[str] = None


class UserModel(BaseModel):
    id: Optional[int] = Field(None, example="123123")
    username: Optional[str] = Field(None, example="@pavel")
    first_name: Optional[str] = Field(None, example="pavel")
    last_name: Optional[str] = Field(None, example="durov")
    photo_url: Optional[str] = Field(
        None,
        example="https://pic.rutube.ru/video/fa/17/fa1763b889c5e26146174f8878315143.jpg",
    )
    telegram_id: int | str


class BasketModel(BaseModel):
    id: int
    photo_url: Optional[str] = None
    author_id: int
    name: str
    is_locked: bool
    created: datetime
    updated: datetime

    @field_serializer("created")
    def created_serializer(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    @field_serializer("updated")
    def updated_serializer(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


class BasketListModel(RootModel[List[BasketModel]]): ...


class BasketDishModel(BaseModel):
    id: int
    user: UserModel
    basket_id: int
    dish: DishModel


class BasketDishListModel(RootModel[List[BasketDishModel]]): ...


class BasketsBasketIdDishesDishIdPostRequestModel(BaseModel):
    user_id: int
    # dish_id: int
    # basket_id: int


class CategoryListModel(RootModel[List[CategoryModel]]): ...


class DishListModel(RootModel[List[DishModel]]):
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


class GetBasketListRequestModel(BaseModel):
    user_id: int


class PrepareMessage(BaseModel):
    id: str
