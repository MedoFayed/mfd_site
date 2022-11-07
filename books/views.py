# books/views.py
from django.views.generic import ListView, DetailView # new
from .models import Book

class BookListView(ListView):
  model = Book
  context_object_name = "book_list" # new (p-180)
  template_name = "books/book_list"


class BookDetailView(DetailView): # new
  model = Book
  context_object_name = "book" # new (p-183)
  template_name = "books/book_detail.html"
