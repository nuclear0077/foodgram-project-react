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

Запустить докер:

```
docker compose up -d --build 
```
Подготовить статику
```
docker compose exec backend python manage.py collectstatic --no-input
```

Зайти
http://localhost/admin
login:admin password:admin
http://localhost
login:test@mail.ru password:test
