# visbox
Visbox

# To build (with new Postgres Docker):
```bash
docker volume create --name=visboxdata
docker-compose build
docker-compose up
docker-compose run web python manage.py migrate
docker-compose run web python manage.py createsuperuser
docker-compose run web python manage.py collectstatic --noinput
```


# To run:
```bash
docker-compose up
```