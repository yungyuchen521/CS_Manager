# CS_Manager

### Requirements
> $ pip install django

> $ pip install djangorestframework

### Setup the Database
create database
> $ touch db.sqlite3

construct the database
> $ python manage.py migrate

create an account for yourself
> $ python manage.py createsuperuser

### Populate the Database
Please use `cases.csv` in `DLPIFP/Database/` on the drive
> $ python manage.py load_cases {path to `cases.csv`}

Please use the `images` folder in `DLPIFP/Database/` on the drive
> $ python manage.py load_tasks {path to `images`}

### Run the System
> $ python manage.py runserver

go to http://127.0.0.1:8000/admin and login with your account
