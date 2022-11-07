# mfd_site/urls.py
# to show the files locally
from django.conf import settings # new
from django.conf.urls.static import static # new

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	# Django admin
	path("admin/", admin.site.urls),
	# User management
	path("accounts/", include("allauth.urls")), # new (p-136)
	# path("accounts/", include("django.contrib.auth.urls")), # new	(Remove p-136)
	# Local apps
  # path("accounts/", include("accounts.urls")), # new page 101 (Remove p-136)
	path("", include("pages.urls")),
	path("books/", include("books.urls")), # new
] + static(
settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
) # new (to show the files locally)


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
