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

engine = create_engine("sqlite:///vaffel.db")


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    photo_url = Column(String)


class Basket(Base):
    __tablename__ = "basket"
    id = Column(Integer, primary_key=True)
    photo_url = Column(String)
    author_id = Column(Integer, ForeignKey(User.id))
    name = Column(String)
    is_locked = Column(Boolean, default=False)
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now(), onupdate=func.now())


class BasketUser(Base):
    __tablename__ = "basket_user"
    id = Column(Integer, primary_key=True)
    basket_id = Column(Integer, ForeignKey(Basket.id))
    user_id = Column(Integer, ForeignKey(User.id))


class Dish(Base):
    __tablename__ = "dish"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    calories = Column(Float)
    proteins = Column(Float)
    fats = Column(Float)
    carbs = Column(Float)
    weight = Column(Float)
    photo_url = Column(Integer, primary_key=True)


class BasketDish(Base):
    __tablename__ = "basket_dish"
    id = Column(Integer, primary_key=True)
    basket_id = Column(Integer, ForeignKey(Basket.id))
    user_id = Column(Integer, ForeignKey(User.id))
    dish_id = Column(Integer, ForeignKey(Dish.id))
    created = Column(DateTime, default=func.now())


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class CategoryDish(Base):
    __tablename__ = "category_dish"
    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey(Dish.id))
    category_id = Column(Integer, ForeignKey(Category.id))


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
