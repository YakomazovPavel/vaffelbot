import json
from sqlalchemy.orm import Session
from database import engine, Dish, Category


def parse_dishes(menu: dict):
    dishes = []
    for item in menu["dishes"]:
        item: dict
        dishes.append(
            Dish(
                id=item.get("id", None),
                name=item.get("name", None),
                description=item.get("description", None),
                price=item.get("price", None),
                calories=item.get("calories", None),
                proteins=item.get("proteins", None),
                fats=item.get("fats", None),
                carbs=item.get("carbs", None),
                weight=item.get("weight", None),
                photo_url=item.get("photo", {}).get("webp", ""),
                category_id=item.get("categoryId", None),
            )
        )

    print(len(dishes))

    with Session(engine) as session:
        session.bulk_save_objects(dishes)
        session.commit()


def parse_categories(menu: dict):
    categories = []
    for item in menu["categories"]:
        item: dict
        categories.append(
            Category(
                id=item.get("id", None),
                name=item.get("name", None),
            )
        )

    print(len(categories))

    with Session(engine) as session:
        session.bulk_save_objects(categories)
        session.commit()


# def parse_category_dishes(menu: dict):
#     category_dishes = []
#     for item in menu["dishes"]:
#         item: dict
#         category_id = item.get("categoryId", None)
#         if category_id is not None:
#             category_dishes.append(
#                 CategoryDish(
#                     dish_id=item.get("id", None),
#                     category_id=category_id,
#                 )
#             )

#     print(len(category_dishes))

#     with Session(engine) as session:
#         session.bulk_save_objects(category_dishes)
#         session.commit()


with open("menu.json", "r") as file:
    menu = json.loads(file.read())
    parse_dishes(menu)
    parse_categories(menu)
    # parse_category_dishes(menu)
