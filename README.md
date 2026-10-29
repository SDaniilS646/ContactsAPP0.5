ContactsApp

Назначение

Веб-приложение на Django для ведения базы компаний, контактов,
сотрудников, материалов и встреч.

Технологии

-   Python 3
-   Django
-   Django ORM
-   HTML/CSS/JavaScript
-   PostgreSQL

Возможности

-   Управление компаниями
-   Управление контактами
-   Управление сотрудниками
-   Управление материалами
-   Управление встречами
-   Авторизация пользователей

Структура

apps/ services/ templates/ static/ config/

Настройка переменных окружения

Перед запуском проекта необходимо создать файл .env в корневой директории проекта (рядом с manage.py) и указать необходимые настройки.

Настройка для production

Перед развёртыванием на сервере необходимо:

Установить DEBUG=False.
Задать ALLOWED_HOSTS, указав домен или IP-адрес сервера.
Установить уникальный надёжный SECRET_KEY.
Убедиться, что файл .env не попадает в систему контроля версий.

Пример файла .env

SECRET_KEY=replace-with-a-secure-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

SECRET_KEY - Секретный ключ Django. Должен быть уникальным и конфиденциальным. Пример: replace-with-a-secure-secret-key
DEBUG - Режим отладки. Включён для локальной разработки, должен быть отключён в production. Пример: True
ALLOWED_HOSTS - Список доменов и IP-адресов, с которых Django принимает запросы. Значения указываются через запятую. Пример: localhost,127.0.0.1

DB_NAME=contacts_db
DB_USER=contacts_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

DB_NAME - Название базы данных PostgreSQL
DB_USER - Имя пользователя PostgreSQL, от имени которого приложение подключается к базе данных.
DB_PASSWORD - Пароль указанного пользователя PostgreSQL.
DB_HOST - Адрес сервера PostgreSQL. Для локальной разработки обычно используется localhost
DB_PORT - Порт PostgreSQL. По умолчанию — 5432

Подготовка базы данных
Установите PostgreSQL и убедитесь, что сервер запущен.

Создайте базу данных и пользователя с необходимыми правами.

Укажите параметры подключения в файле .env.

Запуск

pip install -r requirements.txt 
python manage.py migrate 

При необходимости создайте администратора:
python manage.py createsuperuser

python manage.py runserver

URL: http://127.0.0.1:8000/
