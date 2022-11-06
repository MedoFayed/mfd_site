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
Time to create a migrations file for the changes. We’ll add the optional app name accounts to the command so that only changes to that app are included.
>docker-compose exec web python manage.py makemigrations accounts

>docker-compose exec web python manage.py migrate
-------------------------------
[Custom User Forms]
Create accounts/forms.py
Fill in as shown in app.
Note: --------------------------
	At the very top we’ve imported CustomUser model via get_user_model41 which looks to our AUTH_USER_MODEL config in settings.py. This might feel a bit more circular than directly importing CustomUser here, but it enforces the idea of making one single reference to the custom user model rather than directly referring to it all over our project.
--------------------------------------------------
	Next we import UserCreationForm42 and UserChangeForm43 which will both be extended. Then create two new forms–CustomUserCreationForm and CustomUserChangeForm–that extend the base user forms imported above and specify swapping in our CustomUser model and displaying the fields email and username. The password field is implicitly included by default and so does not need to be explicitly named here as well
--------------------------------------------------
[Custom User Admin] -------------------
Finally we have to update our accounts/admin.py file. The admin is a common place to manipulate user data and there is tight coupling between the built-in User and the admin.
We’ll extend the existing UserAdmin into CustomUserAdmin and tell Django to use our new forms and custom user model. We can also list any user attributes44 we want but for now will just focus on three: email, username, and superuser status.
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
Create new Repo in github (MedoFayed/mfd_site)
update it from local:
git remote add origin https://github.com/MedoFayed/mfd_site.git
git push -u origin main
RESPOND:
d:\#_DEV_Docker\wsv4\mfd_site(main -> origin)
--------------------------------------------------
=====================================================
Chapter 5: Pages App:
----------------------
Let’s build a homepage for our new project.
> docker-compose exec web python manage.py startapp pages
Update INSTALLED_APPS (settings.py).
	"pages.apps.PagesConfig", # new
Update TEMPLATES (settings.py)
	"DIRS": [BASE_DIR / "templates"], # new
>mkdir templates
Create templates/_base.html & templates/home.html

URLs and Views: ------------------
# mysite/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("pages.urls")),
]
----------------------------------
Create pages/urls.py
# pages/urls.py
from django.urls import path
from .views import HomePageView

urlpatterns = [
  path("", HomePageView.as_view(), name="home"),
]
---------------------------------
# pages/views.py
from django.views.generic import TemplateView

class HomePageView(TemplateView):
	template_name = "home.html"
---------------------------------
>docker-compose down
>docker-compose up -d
Test in browser
....
EDIT
# pages/tests.py
from django.test import SimpleTestCase
from django.urls import reverse

class HomepageTests(SimpleTestCase):
  def test_url_exists_at_correct_location(self):
    response = self.client.get("/")
    self.assertEqual(response.status_code, 200)

  def test_homepage_url_name(self):
    response = self.client.get(reverse("home"))
    self.assertEqual(response.status_code, 200)
--------------------------------------------------------
TEST:
RUN:
>docker-compose exec web python manage.py test pages
------------------------------------------------------------
Testing Templates:
Add to # pages/tests.py

  def test_homepage_template(self): # new
    response = self.client.get("/")
    self.assertTemplateUsed(response, "home.html")
--------------------------------------------------
Add to # pages/tests.py
--------------------------------------------------
Testing HTML
Add to # pages/tests.py

  def test_homepage_contains_correct_html(self): # new
    response = self.client.get("/")
    self.assertContains(response, "home page")

  def test_homepage_does_not_contain_incorrect_html(self): # new
    response = self.client.get("/")
    self.assertNotContains(response, "Hi there! I should not be on the page.")
--------------------------------------------------
>docker-compose exec web python manage.py test
===========================================================
setUp()
-------
Resolve:
----------
Git
> git add.
> git commit -m "completed ch5"
> git push -u origin main
--------------------------------------------------
===========================================================
Chapter 6: User Registration
============================
Auth App: -------------
Django provides us with the necessary views and urls which means we only need to update a template for things to work.
* Make sure the auth app is included in our INSTALLED_APPS setting ("django.contrib.auth",).
Auth URLs and Views: -------------
To use Django’s built-in auth app we must explicitly add it to our mfd_site/urls.py file. The easiest approach is to use accounts/ as the prefix.

# mfd_site/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	# Django admin
	path("admin/", admin.site.urls),
	# User management
	path("accounts/", include("django.contrib.auth.urls")), # new
	# Local apps
	path("", include("pages.urls")),
]
"""
# these are automatically included
accounts/login/ [name="login"]
accounts/logout/ [name="logout"]
accounts/password_change/ [name="password_change"]
accounts/password_change/done/ [name="password_change_done"]
accounts/password_reset/ [name="password_reset"]
accounts/password_reset/done/ [name="password_reset_done"]
accounts/reset/<uidb64>/<token>/ [name="password_reset_confirm"]
accounts/reset/done/ [name="password_reset_complete"]
"""
IMPORTANT: Read bottom paragraph of page 90
--------------------------------------------------
Homepage:
Update home.html to tell if user & who is loged in
Check code....
  {% if user.is_authenticated %}
    <p>Hi {{ user.email }}!</p>
  {% else %}
    <p>You are not logged in</p>
    <a href="{% url 'login' %}">Log In</a>
  {% endif %}
--------------------------------------------------
Following the code activated automatically by adding to mysite/urls.py:
	path("accounts/", include("django.contrib.auth.urls")),
-------------------------------
# django/contrib/auth/urls.py
from django.contrib.auth import views
from django.urls import path

urlpatterns = [
	path('login/', views.LoginView.as_view(), name='login'),
	path('logout/', views.LogoutView.as_view(), name='logout'),
	path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
	path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
	path('password_reset/', views.PasswordResetView.as_view(),
	name='password_reset'),
	path('password_reset/done/', views.PasswordResetDoneView.as_view(),
	name='password_reset_done'),
	path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(),
	name='password_reset_confirm'),
	path('reset/done/', views.PasswordResetCompleteView.as_view(),
	name='password_reset_complete'),
]
--------------------------------------------------
try [127.0.0.1:8000/accounts/login] in browser,
Replies:
TemplateDoesNotExist at /accounts/login/
registration/login.html.
------------------------
Create templates/registration/login.html
<!-- templates/registration/login.html -->
{% extends "_base.html" %}

{% block title %}Log In{% endblock title %}

{% block content %}
<h2>Log In</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Log In</button>
</form>
{% endblock content %}
----------------------------------
Then refresh browswer. will show log in
----------------------------------------
Logging in will durect you to [http://127.0.0.1:8000/accounts/profile/]
That does not exist.
Add the following to bottom of settings.py
LOGIN_REDIRECT_URL = "home" # new
--------------------------------------------------
Log Out: ----->
Sign Up: ----->
* Basic steps:
• create an app-level accounts/urls.py file
• update the project-level django_project/urls.py to point to the accounts app
• add a view called SignupPageView
• create a signup.html template file
• update home.html to display the sign up page
1. Create SignupPageView in # accounts/views.py
2. Create # accounts/urls.py & add code.
3. Edit MFD_SITE/urls.py adding:
	path("accounts/", include("accounts.urls")), # new
4. Create templates/registration/signup.html
5. Edit home.html Add: <a href="{% url 'signup' %}">Sign Up</a>
6. Test adding a new user (testuser)
----------------------------------------------------
Tests: ---->
Add SignUpPageTests to accounts/tests.py
Run tests:
>docker-compose exec web python manage.py test
Add setup() to accounts/tests.py (complete change)
------------------------------------------------------------
Git
> git status
> git add .
> git commit -m "Added user registration - ch6"
======================================================================
Chapter 7: Static Assets
1. Local Development
		mkdir static, static/css, static/js, static/images
		create files static/css/base.css, static/js/base.js, static/images/.keep
		-------------
			STATICFILES_DIRS
		In settings.py, add below STATIC_URL = '/static/'
		STATICFILES_DIRS = [BASE_DIR / "static"] # new
		Add to base.css
		Edit _base.html add at the very top:
			{% load static %}
		and after title:
			<link rel="stylesheet" href="{% static 'css/base.css' %}">
		----------------------
		Images
		Add to home.html
		after extends, {% load static %}
		and before the if...
			<img class="bookcover" src="{% static 'images/dfp.jpg' %}">
		--------------------------------------------------
		JavaScript
		Add
		// static/js/base.js
		console.log("JavaScript here!")
		And: befor </body> in _base.html
		<!-- JavaScript -->
		<script src="{% static 'js/base.js' %}"></script>
------------------------------------------------------------------------
2. Production

------------------------------------------------------------------------


------------------------------------------------------------------------


------------------------------------------------------------------------


------------------------------------------------------------------------
-------------------------------