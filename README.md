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

Запуск

pip install -r requirements.txt python manage.py migrate python
manage.py runserver

URL: http://127.0.0.1:8000/
