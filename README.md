# CS_Manager

### Requirements
> $ pip install django

> $ pip install djangorestframework

> $ pip install torch

> $ pip install torchvision

> $ pip install reportlab

### Initialize the Database
create database
> $ touch db.sqlite3

construct the database
> $ python manage.py migrate

### Load static files
> $ python manage.py collectstatic

### Model
Download the model from [here](https://drive.google.com/file/d/10At8oja9Lga58Lyr1uHkx4FYWQTVp4FP/view?usp=share_link) and put it at ./nn_model

### Run the System
> $ python manage.py runserver

go to http://127.0.0.1:8000/upload

### Sample Images
Sample images can be downloaded [here](https://drive.google.com/drive/folders/1VhoRimk7qt2T0TL4GZZmkXF9SP9q6qQL?usp=share_link)
