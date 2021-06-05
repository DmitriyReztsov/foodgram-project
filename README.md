# Foodgram-project
Foodgram
IP: http://84.252.137.97/

![Foodgram-project workflow](https://github.com/DmitriyReztsov/foodgram-project /actions/workflows/main.yml/badge.svg)

# Foodgram

Бэкенд сайта с рецептами. Реализованы сортировка по фиксированным тегам, подписки и избранное, добавление в корзину покупок ингредиентов, вывод в файл списка ингредиентов по всем покупкам.

Взаимодействие с .js реализовано через API.


## Tech

- Python
- Django
- Django Rest Framework
- API
- Gunicorn
- NGINX
- Docker
- DockerHub
- GitHub Actions


## Installation

Выполните на сервере следующие команды:
```sh
docker-compose up -d
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
docker-compose exec web python manage.py dumpdata > fixtures.json
```
Перед первым запуском зайдите в панель администратора и заполните модель Объекты тегов следующими значениями:
| Тег        | Слаг        |
| ---------- |:-----------:|
| Завтрак    | brfst       |
| Обед       | lnch        |
| Ужин       | dnr         |

Зайдите в контейнер web и загрузите ингредиенты:
```sh
sudo docker ps
sudo docker exec -it <CONTAINER_ID> bash
python manage.py load_ingredients
```
При пуше в репозиторий, в ветку master, происходит автоматическая пересборка и перезапуск сайта.



## Author

Dmitriy Reztsov
