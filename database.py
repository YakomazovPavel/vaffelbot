from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase

engine = create_engine("sqlite:///vaffel.db") 

class Base(DeclarativeBase): pass
  
class Dish(Base):
    __tablename__ = 'dish'
    id = Column(Integer, primary_key=True)
    category_id = Column(String)
    name = Column(String)
    description = Column(String)
    price = Column(String)
    calories = Column(String)
    proteins = Column(String)
    fats = Column(String)
    carbs = Column(String)
    weight = Column(String)
    photo_url = Column(String)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)