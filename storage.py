from database import (
    engine,
    User,
    Basket,
    BasketUser,
    BasketDish,
    Dish,
    Category,
)
from sqlalchemy.orm import sessionmaker, joinedload

from models import (
    CategoryModel,
    DishModel,
    UserModel,
    BasketModel,
    BasketDishModel,
    CategoryListModel,
    BasketDishListModel,
    DishListModel,
    BasketListModel,
)
# from sqlalchemy.sql import func


class Storage:
    def __init__(self):
        self.session = sessionmaker(bind=engine)()

    def get_categoryes(self) -> CategoryListModel:
        categoryes = self.session.query(Category).all()
        return CategoryListModel(
            [
                CategoryModel(
                    id=category.id,
                    name=category.name,
                )
                for category in categoryes
            ]
        )

    def get_dishes(self) -> DishListModel:
        dishes = self.session.query(Dish).all()
        return DishListModel(
            [
                DishModel(
                    id=dish.id,
                    category=CategoryModel(
                        id=dish.category.id,
                        name=dish.category.name,
                    )
                    if dish.category
                    else None,
                    name=dish.name,
                    description=dish.description,
                    price=dish.price,
                    calories=dish.calories,
                    proteins=dish.proteins,
                    fats=dish.fats,
                    carbs=dish.carbs,
                    weight=dish.weight,
                    photo_url=dish.photo_url,
                )
                for dish in dishes
            ]
        )

    def get_baskets(self, user_id) -> BasketListModel:
        return BasketListModel(
            [
                BasketModel(
                    id=basket.id,
                    photo_url=basket.photo_url,
                    author_id=basket.author_id,
                    name=basket.name,
                    is_locked=basket.is_locked,
                    created=basket.created,
                    updated=basket.updated,
                )
                for basket in self.session.get(User, user_id).baskets
            ]
        )

    def create_basket(
        self,
        name: str,
        author_id: str,
        photo_url: str | None = None,
    ) -> BasketModel:
        baskets_count = (
            self.session.query(Basket).filter(Basket.author_id == author_id).count()
        )
        photo_url = f"{baskets_count % 10}.jpg"
        basket = Basket(
            name=name,
            author_id=author_id,
            photo_url=photo_url,
        )
        self.session.add(basket)
        self.session.commit()
        self.create_basket_user(
            basket_id=basket.id,
            user_id=author_id,
        )
        return BasketModel(
            id=basket.id,
            photo_url=basket.photo_url,
            author_id=basket.author_id,
            name=basket.name,
            is_locked=basket.is_locked,
            created=basket.created,
            updated=basket.updated,
        )

    def check_basket_user(self, user_id: int, basket_id: int) -> bool:
        return bool(
            self.session.query(BasketUser)
            .filter(BasketUser.user_id == user_id)
            .filter(BasketUser.basket_id == basket_id)
            .first()
        )

    def create_basket_user(self, basket_id, user_id) -> None:
        basket_user = BasketUser(
            basket_id=basket_id,
            user_id=user_id,
        )
        self.session.add(basket_user)
        self.session.commit()

    def create_user(
        self,
        telegram_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        photo_url: str | None = None,
    ) -> UserModel:
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            photo_url=photo_url,
            telegram_id=telegram_id,
        )
        self.session.add(user)
        self.session.commit()
        return UserModel(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            photo_url=user.photo_url,
            telegram_id=user.telegram_id,
        )

    def get_telegram_user(self, telegram_id) -> UserModel | None:
        user = self.session.query(User).filter(User.telegram_id == telegram_id).first()
        if user:
            return UserModel(
                id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                photo_url=user.photo_url,
                telegram_id=user.telegram_id,
            )

    def get_basket_by_id(self, id) -> Basket | None:
        return self.session.query(Basket).filter(Basket.id == id).first()

    def check_user_id(self, id) -> bool:
        return bool(self.session.query(User.id).filter(User.id == id).first())

    def get_user_by_id(self, id: int) -> UserModel | None:
        user = self.session.query(User).filter(User.id == id).first()
        print(f"!get_user_by_id user.telegram_id {user.telegram_id}")
        if user:
            return UserModel(
                id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                photo_url=user.photo_url,
                telegram_id=user.telegram_id,
            )

    def get_dish_by_id(self, id) -> Dish | None:
        return self.session.query(Dish).filter(Dish.id == id).first()

    def create_basket_dish(
        self,
        basket_id,
        user_id,
        dish_id,
    ) -> BasketDishModel:
        basket_dish = BasketDish(
            basket_id=basket_id,
            user_id=user_id,
            dish_id=dish_id,
        )
        self.session.add(basket_dish)
        self.session.commit()

        return BasketDishModel(
            id=basket_dish.id,
            user=UserModel(
                id=basket_dish.user.id,
                username=basket_dish.user.username,
                first_name=basket_dish.user.first_name,
                last_name=basket_dish.user.last_name,
                photo_url=basket_dish.user.photo_url,
                telegram_id=basket_dish.user.telegram_id,
            ),
            basket_id=basket_dish.basket_id,
            dish=DishModel(
                id=basket_dish.dish.id,
                category=CategoryModel(
                    id=basket_dish.dish.category.id,
                    name=basket_dish.dish.category.name,
                )
                if basket_dish.dish.category
                else None,
                name=basket_dish.dish.name,
                description=basket_dish.dish.description,
                price=basket_dish.dish.price,
                calories=basket_dish.dish.calories,
                proteins=basket_dish.dish.proteins,
                fats=basket_dish.dish.fats,
                carbs=basket_dish.dish.carbs,
                weight=basket_dish.dish.weight,
                photo_url=basket_dish.dish.photo_url,
            ),
        )

    def get_basket_dishes(self, basket_id) -> BasketDishListModel:
        return BasketDishListModel(
            [
                BasketDishModel(
                    id=basket_dish.id,
                    user=UserModel(
                        id=basket_dish.user.id,
                        username=basket_dish.user.username,
                        first_name=basket_dish.user.first_name,
                        last_name=basket_dish.user.last_name,
                        photo_url=basket_dish.user.photo_url,
                        telegram_id=basket_dish.user.telegram_id,
                    ),
                    basket_id=basket_dish.basket_id,
                    dish=DishModel(
                        id=basket_dish.dish.id,
                        category=CategoryModel(
                            id=basket_dish.dish.category.id,
                            name=basket_dish.dish.category.name,
                        )
                        if basket_dish.dish.category
                        else None,
                        name=basket_dish.dish.name,
                        description=basket_dish.dish.description,
                        price=basket_dish.dish.price,
                        calories=basket_dish.dish.calories,
                        proteins=basket_dish.dish.proteins,
                        fats=basket_dish.dish.fats,
                        carbs=basket_dish.dish.carbs,
                        weight=basket_dish.dish.weight,
                        photo_url=basket_dish.dish.photo_url,
                    ),
                )
                for basket_dish in self.session.query(BasketDish)
                .filter(BasketDish.basket_id == basket_id)
                .all()
            ]
        )

    def check_basket_id(self, id) -> bool:
        return bool(self.session.query(Basket.id).filter(Basket.id == id).first())

    def remove_basket_dish(
        self, basket_id: int, dish_id: int
    ) -> BasketDishModel | None:
        basket_dish = (
            self.session.query(BasketDish)
            .options(joinedload(BasketDish.user))
            .filter_by(basket_id=basket_id, dish_id=dish_id)
            .first()
        )
        if basket_dish:
            self.session.delete(basket_dish)
            self.session.commit()
            return BasketDishModel(
                id=basket_dish.id,
                user=UserModel(
                    id=basket_dish.user.id,
                    username=basket_dish.user.username,
                    first_name=basket_dish.user.first_name,
                    last_name=basket_dish.user.last_name,
                    photo_url=basket_dish.user.photo_url,
                    telegram_id=basket_dish.user.telegram_id,
                ),
                basket_id=basket_dish.basket_id,
                dish=DishModel(
                    id=basket_dish.dish.id,
                    category=CategoryModel(
                        id=basket_dish.dish.category.id,
                        name=basket_dish.dish.category.name,
                    )
                    if basket_dish.dish.category
                    else None,
                    name=basket_dish.dish.name,
                    description=basket_dish.dish.description,
                    price=basket_dish.dish.price,
                    calories=basket_dish.dish.calories,
                    proteins=basket_dish.dish.proteins,
                    fats=basket_dish.dish.fats,
                    carbs=basket_dish.dish.carbs,
                    weight=basket_dish.dish.weight,
                    photo_url=basket_dish.dish.photo_url,
                ),
            )

    def get_inline_baskets(self, telegram_id: int, basket_name: str) -> BasketListModel:
        baskets = (
            self.session.query(Basket)
            .join(BasketUser, Basket.id == BasketUser.basket_id)
            .join(User, BasketUser.user_id == User.id)
            .filter(User.telegram_id == telegram_id)
            .filter(Basket.name.icontains(basket_name))
            .all()
        )

        print(f"!get_inline_baskets {baskets}")

        return BasketListModel(
            [
                BasketModel(
                    id=basket.id,
                    photo_url=basket.photo_url,
                    author_id=basket.author_id,
                    name=basket.name,
                    is_locked=basket.is_locked,
                    created=basket.created,
                    updated=basket.updated,
                )
                for basket in baskets
                # self.session.query(User)
                # .join(Basket)
                # .filter(User.telegram_id == telegram_id)
                # .filter(Basket.name.contains(name))
                # .first()
                # .baskets
            ]
        )


storage = Storage()
