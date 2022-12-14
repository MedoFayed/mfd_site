# books/views.py
from django.contrib.auth.mixins import (
  LoginRequiredMixin,
  PermissionRequiredMixin # new
)
from django.views.generic import ListView, DetailView # new
from .models import Book

class BookListView(
    LoginRequiredMixin, 
    ListView):
  model = Book
  context_object_name = "book_list" # new (p-180)
  template_name = "books/book_list"
  login_url = "account_login" # new
  


class BookDetailView(
    LoginRequiredMixin, 
    PermissionRequiredMixin,  # new
    DetailView): # new
  model = Book
  context_object_name = "book" # new (p-183)
  template_name = "books/book_detail.html"
  login_url = "account_login" # new
  permission_required = "books.special_status" # new