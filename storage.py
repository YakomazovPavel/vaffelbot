from sqlalchemy import select
from database import engine
from sqlalchemy.orm import sessionmaker
from typing import List
from models import Category


class Storage:
    def __init__(self):
        self.session = sessionmaker(bind=engine)()

    def get_categoryes(self) -> List[Category]:
        statement = select(Category)
        result = self.session.execute(statement)
        return result.scalars().all()

    def get_dishes(self) -> List[Dish]:
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

    def get_baskets(self) -> List[Basket]:
        statement = select(Basket)
        result = self.session.execute(statement)
        return result.scalars().all()

    def create_basket(
        self,
        name: str,
        author_id: str,
        photo_url: str | None = None,
    ) -> Basket:
        basket = Basket(
            name=name,
            author_id=author_id,
            photo_url=photo_url,
        )
        self.session.add(basket)
        self.session.commit()
        return basket

    def create_user(
        self,
        telegram_id: str,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        photo_url: str | None = None,
    ) -> User:
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            photo_url=photo_url,
            telegram_id=telegram_id,
        )
        self.session.add(user)
        self.session.commit()
        return user

    def get_telegram_user(self, telegram_id) -> User | None:
        return self.session.query(User).filter(User.telegram_id == telegram_id).first()

    def get_basket_by_id(self, id) -> Basket | None:
        return self.session.query(Basket).filter(Basket.id == id).first()

    def get_user_by_id(self, id) -> User | None:
        return self.session.query(User).filter(User.id == id).first()

    def get_dish_by_id(self, id) -> User | None:
        return self.session.query(Dish).filter(Dish.id == id).first()

    def create_basket_dish(
        self,
        basket_id,
        user_id,
        dish_id,
    ) -> BasketDish:
        basket_dish = BasketDish(
            basket_id=basket_id,
            user_id=user_id,
            dish_id=dish_id,
        )
        self.session.add(basket_dish)
        self.session.commit()
        return basket_dish

    def get_basket_dishes(
        self,
        basket_id) -> List[]:
        ...

storage = Storage()