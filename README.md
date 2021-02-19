## Starting
- Check requirements.txt

- Run `python manage.py runserver`

## Admin Panel

- Go to http://127.0.0.1:8000/admin 
- New admin: `python manage.py createsuperuser`

## Migrations

- Make migrations when you make changes in the **models.py**. First use the following command: 

`python manage.py makemigrations`

- then:

`python manage.py migrate`

## Notes About Templates

- Use `{% load static %}` in the first line of the html files.
- The correct way of using static paths: `{% static 'path_to_your_static_file.extension' %}`

## Notes and Codes

- Create a new app:

`python manage.py startapp <appname>`






