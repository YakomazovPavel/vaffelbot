import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from type import Dish
 
app = FastAPI()
 
@app.get("/users/{id}/", tags=["Users"])
def read_root(id: str):
    return {"data": id}

@app.get("/dishes/", tags=["Dishes"])
def get_dishes():
    # Получить инфу из бд
    # Построить ответ в формате json
    return {"data": "Hello World"}


if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=3000, workers=1)