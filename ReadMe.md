Create requirements.txt
	Django==4.1.3
	psycopg2-binary

d:\#_DEV_Docker\wsv4\mfd_site\
> py -m venv .venv
> .venv\scripts\activate
(.venv)> py -m pip install -r requirements.txt
(.venv)> py -m pip install --upgrade pip
(.venv)> django-admin startproject mysite .
(.venv)> py manage.py migrate [optional]
(.venv)> py manage.py runserver
Check in browser (127.0.0.1:8000) --->
(.venv)> pip freeze > requirements.txt
Docker --->
(.venv)> deactivate
Create [Dockerfile] & [docker-compose.yml] & Add
[Dockerfile]:
-------------------------------
# Pull base image
FROM python:3.10.4-slim-bullseye
# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /code
# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# Copy project
COPY . .
-------------------------------
Create [.dockerignore]
-------------------------------
.venv
.git
.gitignore
-------------------------------
Create [.gitignore]
-------------------------------
.venv
__pycache__/
db.sqlite3
#.DS_Store # Mac only
-------------------------------
>docker-compose up -d --build
Check in browser (127.0.0.1:8000) --->
<-- it is running now from container -->
------------------------------------------------
<-- My notes -->
Any Edit to the local code should be followed by
>docker down
>docker-compose up -d --build
TO rebuild the image using the updates
------------------------------------------------
[PostgreSQL]
Update DATABASE in settings.py
-------------------------------
DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.postgresql",
		"NAME": "postgres",
		"USER": "postgres",
		"PASSWORD": "postgres",
		"HOST": "db",
		"PORT": 5432,
	}
}
--------------------------------------------------
>docker-compose down
>docker-compose up -d --build
--------------------------------------------------
[Custom User Model]
1. Create a CustomUser model
2. Update django_project/settings.py
3. Customize UserCreationForm and UserChangeForm
4. Add the custom user model to admin.py
--------------------------------------------------

<-- This is how to access the container from outside -->
> docker-compose exec web python manage.py startapp accounts
1.1.
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
	pass
2.
# django_project/settings.py
INSTALLED_APPS = [
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.messages",
	"django.contrib.staticfiles",
	# Local
	"accounts.apps.AccountsConfig", # new
]
...
AUTH_USER_MODEL = "accounts.CustomUser" # new
2.2.
Time to create a migrations file for the changes. We�ll add the optional app name accounts to the command so that only changes to that app are included.
>docker-compose exec web python manage.py makemigrations accounts

>docker-compose exec web python manage.py migrate
-------------------------------
[Custom User Forms]
Create accounts/forms.py
Fill in as shown in app.
Note: --------------------------
	At the very top we�ve imported CustomUser model via get_user_model41 which looks to our AUTH_USER_MODEL config in settings.py. This might feel a bit more circular than directly importing CustomUser here, but it enforces the idea of making one single reference to the custom user model rather than directly referring to it all over our project.
--------------------------------------------------
	Next we import UserCreationForm42 and UserChangeForm43 which will both be extended. Then create two new forms�CustomUserCreationForm and CustomUserChangeForm�that extend the base user forms imported above and specify swapping in our CustomUser model and displaying the fields email and username. The password field is implicitly included by default and so does not need to be explicitly named here as well
--------------------------------------------------
[Custom User Admin] -------------------
Finally we have to update our accounts/admin.py file. The admin is a common place to manipulate user data and there is tight coupling between the built-in User and the admin.
We�ll extend the existing UserAdmin into CustomUserAdmin and tell Django to use our new forms and custom user model. We can also list any user attributes44 we want but for now will just focus on three: email, username, and superuser status.
--------------------------------------------------
# accounts/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
  add_form = CustomUserCreationForm
  form = CustomUserChangeForm
  model = CustomUser
  list_display = [
    "email",
    "username",
    "is_superuser",
  ]

admin.site.register(CustomUser, CustomUserAdmin)
--------------------------------------------------
Phew. A bit of code upfront but this saves a ton of heartache later on.
--------------------------------------------------
[Superuser] -------------
>docker-compose exec web python manage.py createsuperuser
admin, admin@me.com, testpass123
--------------------------------------------------
NOTE: container is still running, test in browser & login to admin !!! not true
--------------------------------------------------
>docker-compose down
>docker-compose up -d
Login admin in the browser
--------------------------------------------------
[Tests] --------------
[Unit Tests] --------------
Read page 72,...
# accounts/tests.py
from django.contrib.auth import get_user_model
from django.test import TestCase

class CustomUserTests(TestCase):
	def test_create_user(self):
		User = get_user_model()
		user = User.objects.create_user(
		username="will", email="will@email.com", password="testpass123")
		self.assertEqual(user.username, "will")
		self.assertEqual(user.email, "will@email.com")
		self.assertTrue(user.is_active)
		self.assertFalse(user.is_staff)
		self.assertFalse(user.is_superuser)

	def test_create_superuser(self):
		User = get_user_model()
		admin_user = User.objects.create_superuser(
			username="superadmin", email="superadmin@email.com", password="testpass123")
		self.assertEqual(admin_user.username, "superadmin")
		self.assertEqual(admin_user.email, "superadmin@email.com")
		self.assertTrue(admin_user.is_active)
		self.assertTrue(admin_user.is_staff)
		self.assertTrue(admin_user.is_superuser)
--------------------------------------------------
>docker-compose exec web python manage.py test
--------------------------------------------------
[Git] --------------------
>git init
>git status
>git add .
>git commit -m "initial commit"
>git status
RESPOND:
>d:\#_DEV_Docker\wsv4\mfd_site(main)
--------------------------------------------------



--------------------------------------------------


--------------------------------------------------


--------------------------------------------------


--------------------------------------------------
-------------------------------

> 
> 
> 

-------------------------------