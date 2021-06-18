# 2D73E461A0E0A584
Test for alytics

#### Регистрация участников

Регистрация пользователя происходит на главной странице сайта.

Любой зарегистрировавшийся имеет доступ к таблицам функций в админке.

Сайт может запускаться на локальном сервере и в докер контейнерах.

### Клонирование репозитория из GitHub:
Войти в нужную директорию на своем компьютере и выполнить команду
```bash
$ git clone https://github.com/Vitaly535/2D73E461A0E0A584

```

#### Заполнение базы начальными данными

 Выполнить миграцию базы данных в postgresql:
  
```bash
~/foodgram$ docker-compose exec web python manage.py migrate --noinput
```
Существует возможность того, что не все миграции выполнены, в этом случае необходимо продублировать миграцию по приложениям:
```bash
docker-compose exec web python manage.py makemigrations funcapp
docker-compose exec web python manage.py migrate --noinput
```
 Чтобы заполнить базу начальными данными из файла fixtures.json необходимо выполнить следующую последовательность:
 - для удаления старых данных зайти на приложение в контейнере:
 ```bash
 docker-compose exec web python manage.py shell
  >>>from django.contrib.contenttypes.models import ContentType
  >>>ContentType.objects.all().delete()
  >>>quit()
 ```
 - для загрузки из файла выполнить:
 ```bash
 docker-compose exec web python manage.py loaddata fixtures.json
 ```

#### Создание суперпользователя
```bash
docker-compose exec web python manage.py createsuperuser
```
Заполнить требуемые поля: email адрес, username, пароль (с подтверждением)

#### Сбор статических файлов для правильного отображения
```bash
docker-compose exec web python manage.py collectstatic
```