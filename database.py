from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
    select,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.sql import func
from dotenv import load_dotenv
from os import getenv
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv()
PATH_TO_DB = getenv(
    "PATH_TO_DB", default="sqlite:////home/YakomazovPavel/vaffelbot/vaffel.db"
)
logger.error("PATH_TO_DB", PATH_TO_DB)
print("print PATH_TO_DB", PATH_TO_DB)
engine = create_engine(PATH_TO_DB)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)


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
    id = Column(Integer, primary_key=True, autoincrement=True)
    basket_id = Column(Integer, ForeignKey(Basket.id))
    user_id = Column(Integer, ForeignKey(User.id))


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


class BasketDish(Base):
    __tablename__ = "basket_dish"
    id = Column(Integer, primary_key=True, autoincrement=True)
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
    id = Column(Integer, primary_key=True, autoincrement=True)
    dish_id = Column(Integer, ForeignKey(Dish.id))
    category_id = Column(Integer, ForeignKey(Category.id))


class Storage:
    def __init__(self):
        self.session = sessionmaker(bind=engine)()

    def get_categoryes(self) -> list[Category]:
        statement = select(Category)
        result = self.session.execute(statement)
        return result.scalars().all()

    def get_dishes(self) -> list[Dish]:
        # statement = select(Dish, CategoryDish.category_id).join(
        #     CategoryDish, Dish.id == CategoryDish.dish_id
        # )
        # result = self.session.execute(statement)
        # print(result)
        # return result.scalars().all()

        return (
            self.session.query(Dish, CategoryDish.category_id)
            .join(CategoryDish, Dish.id == CategoryDish.dish_id)
            .all()
        )


storage = Storage()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
