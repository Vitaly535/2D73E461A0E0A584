# 2D73E461A0E0A584
Test for alytics

### Регистрация участников

Регистрация пользователя происходит на главной странице сайта.

Любой зарегистрировавшийся имеет доступ к таблицам функций в админке.

Сайт может запускаться на локальном сервере и в докер контейнерах.

### Клонирование репозитория из GitHub:
Войти в нужную директорию на своем компьютере и выполнить команду
```bash
$ git clone https://github.com/Vitaly535/2D73E461A0E0A584

```
### Запуск приложения на локальном сервере, БД sqlite3
В директории, куда был клонирован код, создать виртуальное окружение:
```bash
<path>/2D73E461A0E0A584$ python3 -m venv venv
```
Запустить виртуальное окружение:
```bash
<path>/2D73E461A0E0A584$ source venv/bin/activate
```
Загрузить в него необходимое программное обеспечение:
```bash
(venv)<path>/2D73E461A0E0A584$ pip3 install -r requirements.txt
```
Запустить локальный сервер
```bash
(venv)<path>/2D73E461A0E0A584$ python manage.py runserver
```
Провести миграцию базы данных, создать необходимые таблицы:
```bash
(venv)<path>/2D73E461A0E0A584$ python manage.py migrate
```
Создать суперпользователя:
```bash
(venv)<path>/2D73E461A0E0A584$ python manage.py createsuperuser
```
Собрать статические файлы:
```bash
(venv)<path>/2D73E461A0E0A584$ python manage.py collectstatic
```
Для работы приложения необходимо запустить на локальной машине сервер Redis и
worker Celery. Они уже установлены в виртуальном окружении.
 Из отдельных терминалов выполнить:
```bash
(venv)<path>/2D73E461A0E0A584$ redis-server
(venv)<path>/2D73E461A0E0A584$ celery -A alyticstest worker -l info
```
Проверка работы redis-server:
```bash
(venv)<path>/2D73E461A0E0A584$ redis-cli ping
PONG
```

По умолчанию, приложение находится по адресу: http://127.0.0.1:8000


### Запуск приложения в докер-контейнерах локально

Создать файл .env в корневом каталоге приложения
Пример файла:

```bash
DB_NAME=xxxxxxxx
POSTGRES_USER=xxxxxxxx
POSTGRES_PASSWORD=xxxxxxxx
DB_HOST=db
DB_PORT=5432
```
Для удобства, поля DB_NAME и POSTGRES_USER могут быть идентичными, при этом
создается одноименная база данных.(Если это не противоречит политике 
безопасности). ВАЖНО: суперпользователь PostgreSQL создается при создании 
VOLUME в докер-контейнерах, в дальнейшем изменить параметры проблематично. 
Вариант - удалить VOLUME и создать новый с новыми параметрами, предварительно
сохранив имеемую базу.

### Установка необходимых компонентов
#### Программа Docker 
Ссылка на официальный сайт: https://docs.docker.com/engine/install/

#### Программа Docker-compose
Ссылка на официальный сайт: https://docs.docker.com/compose/install/

### Запуск приложения

Проект запускается в docker контейнерах. Из корневой директории проекта, 
после установки необходимых компонентов, выполнить команду:
```bash
 <path>/2D73E461A0E0A584$ docker-compose up -d --build
```
#### Создание базы данных в VOLUME Postgres (если имеет другое имя)
Контейнер db (postgres) должен быть запущен.
```bash
<path>/2D73E461A0E0A584$ docker-compose exec db bash
root@xxxxxxxxxx:/# psql -U xxxxxxxx
xxxxxxxx=# CREATE DATABASE yyyyyyyy;
CREATE DATABASE
xxxxxxxx=# \q
```
#### Заполнение базы начальными данными
Все команды производятся при запущеных и стабильно работающих контейнерах.
 Выполнить миграцию базы данных в postgresql:
  
```bash
<path>/2D73E461A0E0A584$ docker-compose exec web python manage.py migrate --noinput
```
Существует возможность того, что не все миграции выполнены,
 в этом случае необходимо продублировать миграцию по приложениям:
```bash
<path>/2D73E461A0E0A584$ docker-compose exec web python manage.py makemigrations funcapp
<path>/2D73E461A0E0A584$ docker-compose exec web python manage.py migrate --noinput
```
 Чтобы заполнить базу начальными данными из файла fixtures.json необходимо 
 выполнить следующую последовательность:
 - для удаления старых данных зайти на приложение в контейнере:
 ```bash
 <path>/2D73E461A0E0A584$ docker-compose exec web python manage.py shell
  >>>from django.contrib.contenttypes.models import ContentType
  >>>ContentType.objects.all().delete()
  >>>quit()
 ```
 - для загрузки из файла выполнить:
 ```bash
 <path>/2D73E461A0E0A584$ docker-compose exec web python manage.py loaddata fixtures.json
 ```

#### Создание суперпользователя
```bash
<path>/2D73E461A0E0A584$ docker-compose exec web python manage.py createsuperuser
```
Заполнить требуемые поля: email адрес, username, пароль (с подтверждением)

#### Сбор статических файлов для правильного отображения
```bash
<path>/2D73E461A0E0A584$ docker-compose exec web python manage.py collectstatic
```