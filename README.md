# FOODGRAM
![example workflow](https://github.com/nuclear0077/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
## О проекте
Платформа Foodgram, «Продуктовый помощник». Онлайн-сервис и API для него.
На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов,
необходимых для приготовления одного или нескольких выбранных блюд.

## Технологии
Python 3.7, Django 3.2, DRF 3.12, drf-spectacular, Djoser, Postgres, Authtoken

## Документация

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
## Описание функционала

### Главная страница
Содержимое главной страницы — список первых шести рецептов, отсортированных по дате публикации (от новых к старым).  Остальные рецепты доступны на следующих страницах: внизу страницы есть пагинация.

### Страница рецепта
На странице — полное описание рецепта. Для авторизованных пользователей — возможно добавить рецепт в избранное и в список покупок а также подписаться на автора рецепта.

### Страница пользователя
На странице — имя пользователя, все рецепты, опубликованные пользователем и подписаться на пользователя.

### Подписка на авторов
Подписка на публикации доступна только авторизованному пользователю. Страница подписок доступна только владельцу.

#### Сценарий поведения пользователя:

Пользователь переходит на страницу другого пользователя или на страницу рецепта и подписывается на публикации автора кликом по кнопке «Подписаться на автора».

Пользователь переходит на страницу «Мои подписки» и просматривает список рецептов, опубликованных теми авторами, на которых он подписался. Сортировка записей — по дате публикации (от новых к старым).

При необходимости пользователь может отказаться от подписки на автора: переходит на страницу автора или на страницу его рецепта и нажимает «Отписаться от автора»

### Список избранного

Работа со списком избранного доступна только авторизованному пользователю.

Список избранного может просматривать только его владелец.

Сценарий поведения пользователя:

Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в избранное».

Пользователь переходит на страницу «Список избранного» и просматривает персональный список избранных рецептов.

При необходимости пользователь может удалить рецепт из избранного.

### Список покупок

Работа со списком покупок доступна авторизованным пользователям. Список покупок может просматривать только его владелец.

Сценарий поведения пользователя:

Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в покупки».

Пользователь переходит на страницу Список покупок, там доступны все добавленные в список рецепты. Пользователь нажимает кнопку Скачать список и получает файл с суммированным перечнем и количеством необходимых ингредиентов для всех рецептов, сохранённых в «Списке покупок».

При необходимости пользователь может удалить рецепт из списка покупок.

Список покупок скачивается в формате .txt (или, по желанию, можно сделать выгрузку PDF).

При скачивании списка покупок ингредиенты в результирующем списке не  дублируются; если в двух рецептах есть сахар (в одном рецепте 5 г, в другом — 10 г), то в списке один пункт: Сахар — 15 г.

### Фильтрация по тегам

При нажатии на название тега выводится список рецептов, отмеченных этим тегом. Фильтрация может проводится по нескольким тегам в комбинации «или»: если выбраны несколько тегов — в результате должны быть показаны рецепты, которые отмечены хотя бы одним из этих тегов.

При фильтрации на странице пользователя фильтруются только рецепты выбранного пользователя. Такой же принцип должен соблюдаться при фильтрации списка избранного.

### Регистрация и авторизация

В проекте реализована система регистрации и авторизации пользователей.

#### Обязательные поля для пользователя:
+ Логин
+ Пароль
+ Email
+ Имя
+ Фамилия

#### Уровни доступа пользователей:
+ Гость (неавторизованный пользователь)
+ Авторизованный пользователь
+ Администратор

#### Что могут делать неавторизованные пользователи
+ Создать аккаунт.
+ Просматривать рецепты на главной.
+ Просматривать отдельные страницы рецептов.
+ Просматривать страницы пользователей.
+ Фильтровать рецепты по тегам.

#### Что могут делать авторизованные пользователи
+ Входить в систему под своим логином и паролем.
+ Выходить из системы (разлогиниваться).
+ Менять свой пароль.
+ Создавать/редактировать/удалять собственные рецепты
+ Просматривать рецепты на главной.
+ Просматривать страницы пользователей.
+ Просматривать отдельные страницы рецептов.
+ Фильтровать рецепты по тегам.
+ Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов.
+ Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл с количеством необходимых ингридиентов для рецептов из списка покупок.
+ Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.

#### Что может делать администратор

+ Администратор обладает всеми правами авторизованного пользователя.
+ Плюс к этому он может:
+ изменять пароль любого пользователя,
+ создавать/блокировать/удалять аккаунты пользователей,
+ редактировать/удалять любые рецепты,
+ добавлять/удалять/редактировать ингредиенты.
+ добавлять/удалять/редактировать теги.
+ Все эти функции нужно реализовать в стандартной админ-панели Django.


### Документация API.
Для просмотра документации необходимо запустить проект и перейти по ссылке http://84.201.151.241/api/schema/swagger-ui/ или http://84.201.151.241/api/schema/redoc

### Тестирование проекта
Вход в административное меню.
http://84.201.151.241/admin

Вход под обычным пользователем.
login:admin password:admin
http://84.201.151.241/
login:test@mail.ru password:12345678pass
