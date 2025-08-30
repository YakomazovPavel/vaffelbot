from typing import Optional
from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    username: Optional[str] = Field(None, example="pavel_yakomazov")
    first_name: Optional[str] = Field(None, example="pavel")
    last_name: Optional[str] = Field(None, example="")
    photo_url: Optional[str] = Field(
        None,
        example="https://pic.rutube.ru/video/fa/17/fa1763b889c5e26146174f8878315143.jpg",
    )
    telegram_id: int


class CreateBasketRequest(BaseModel):
    author_id: int
    name: str
