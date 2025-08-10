# vaffel_tg

backend for vaffel_tg bot

## Запуск проекта

1. Создать виртуальное окружение

```
python3 -m venv .venv
```

2. Активировать виртуальное окружение

```
. .venv/bin/activate
```

4. Установить зависимости

```
pip install -r requirements.txt
```

5. Запустить проект

```
python main.py
```

## Помощь

Применить изменение таблиц в бд

```
python database.py
```

## Кодогенерация

```
pip install fastapi-code-generator
```

```
fastapi-codegen --input openapi.yml --output app
```
