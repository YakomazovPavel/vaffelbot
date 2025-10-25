from typing import List
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from dotenv import load_dotenv
from os import getenv
import logging

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv()
PATH_TO_DB = getenv(
    "PATH_TO_DB", default="sqlite:////home/YakomazovPavel/vaffelbot/vaffel.db"
)
engine = create_engine(PATH_TO_DB)


# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#association-object


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
    telegram_id = Column(Integer, nullable=False, unique=True)
    baskets: Mapped[List["Basket"]] = relationship(
        back_populates="users", secondary="basket_user"
    )


class Basket(Base):
    __tablename__ = "basket"
    id = Column(Integer, primary_key=True)
    photo_url = Column(String)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    users: Mapped[List["User"]] = relationship(
        back_populates="baskets",
        secondary="basket_user",
    )
    name = Column(String)
    is_locked = Column(Boolean, default=False)
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now(), onupdate=func.now())


class BasketUser(Base):
    __tablename__ = "basket_user"
    basket_id: Mapped[int] = mapped_column(ForeignKey("basket.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)


class BasketDish(Base):
    __tablename__ = "basket_dish"
    id = Column(Integer, primary_key=True, autoincrement=True)
    basket_id: Mapped[int] = mapped_column(ForeignKey("basket.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    dish_id: Mapped[int] = mapped_column(ForeignKey("dish.id"))
    basket: Mapped["Basket"] = relationship()
    user: Mapped["User"] = relationship()
    dish: Mapped["Dish"] = relationship()
    created = Column(DateTime, default=func.now())


class Dish(Base):
    __tablename__ = "dish"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    calories = Column(Float, nullable=True)
    proteins = Column(Float, nullable=True)
    fats = Column(Float, nullable=True)
    carbs = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    photo_url = Column(String, nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship()
    color = Column(String, nullable=True)


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String)


# if __name__ == "__main__":
#     Base.metadata.create_all(bind=engine)
