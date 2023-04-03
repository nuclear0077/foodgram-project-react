## FOODGRAM

## About


## Technology


## Documentation

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/nuclear0077/foodgram-project-react.git
```

```
cd foodgram-project-react/infra/
```

Указать настройки для подключения к СУБД Postgres в файле .env для этого необходимо переименовать .env.example файл на .env
Создадим файл
```
cp .env.example .env
```

Выполнить команду
```
docker compose up -d --build  
```

Инициализировать базу данных

```
docker compose exec db createdb -U postgres foodgram
```

Применить миграции

```
docker compose exec backend python manage.py migrate
```

Подготовить статику

```
docker compose exec backend python manage.py collectstatic --no-input 
```

Загрузить данные из JSON
```
docker compose exec backend python manage.py loaddata fixtures.json
```
Зайти
http://localhost/admin
login:admin password:admin
http://localhost
login:test@mail.ru password:test




