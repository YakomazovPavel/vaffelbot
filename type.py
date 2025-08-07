from pydantic import BaseModel

class Dish(BaseModel):
    id: str
    category_id: str
    name: str
    description: str
    price: float
    calories: float
    proteins: float
    fats: float
    carbs: float
    weight: float
    photo_url: str