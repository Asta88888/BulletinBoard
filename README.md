# Дипломный проект: "Доска объявлений"
1. ### Описание проекта

#### Проект представляет собой backend платформы для публикации объявлений с функционалом:
* Регистрация и аутентификация пользователей.
* Роли пользователей: user и admin.
* Сброс и восстановление пароля через email.
* CRUD для объявлений (только автор или админ может редактировать/удалять).
* CRUD для отзывов под объявлениями.
* Поиск объявлений по названию.
* Пагинация объявлений (4 на странице).
* Автогенерация документации API (Swagger / ReDoc).

2. ### Технологии
* Python 3.10+
* Django 4.x
* Django REST Framework
* Simple JWT (JWT аутентификация)
* PostgreSQL (основная БД)
* django-filter (фильтры и поиск)
* drf-yasg (Swagger / ReDoc)
* django-cors-headers (CORS)
* Docker & Docker-Compose
* pytest + DRF test framework (тестирование)

3. ### Модели
#### User
* Поля: email, first_name, last_name, phone, role (user/admin), image.
* Особенности: email используется как логин.

#### Ad (Объявление)
* Поля: title, price, description, author, created_at.
* Сортировка: по created_at (новые сверху).

#### Review (Отзыв)
* Поля: text, author, ad, created_at.
* Сортировка: по created_at.

4. ### Permissions
* Аноним: просмотр списка объявлений.
* Пользователь: CRUD своих объявлений и отзывов.
* Админ: CRUD любых объявлений и отзывов.

5. ### Тестирование
* Тестируются: CRUD, права доступа, фильтры, поиск, пагинация.

6. ### Swagger / ReDoc
* Swagger UI: /swagger/
* ReDoc: /redoc/
* Настроено через drf_yasg с публичным доступом.

7. ### Запуск проекта
* Скопировать .env.example в .env и заполнить переменные

* Запустить проект через Docker:
docker-compose up --build

* Применить миграции:
docker-compose exec web python manage.py migrate

* Создать суперпользователя:
docker-compose exec web python manage.py createsuperuser

* Swagger: http://localhost:8000/swagger/
* ReDoc: http://localhost:8000/redoc/
* Django admin: http://localhost:8000/admin/
