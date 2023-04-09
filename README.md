# FOODGRAM
![example workflow](https://github.com/nuclear0077/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
## About
Платформа Foodgram, «Продуктовый помощник». Онлайн-сервис и API для него. 
На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, 
необходимых для приготовления одного или нескольких выбранных блюд.

## Technology
Python 3.7, Django 3.2, DRF 3.12, drf-spectacular, Djoser, Postgres, Authtoken

## Documentation

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/nuclear0077/foodgram-project-react.git
```

```
cd foodgram-project-react/
```

Запустить проект используя команду
```
make start
```

Загрузить дамп базы
```
make load_dump
```

Остановить проект
```
make stop
```

Удалить докер контейнеры
```
make drop
```

### Документация API.
Для просмотра документации необходимо запустить проект и перейти по ссылке http://84.201.151.241/api/schema/swagger-ui/ или http://84.201.151.241/api/schema/redoc


Зайти
http://84.201.151.241/admin
login:admin password:admin
http://84.201.151.241/
login:test@mail.ru password:12345678pass
