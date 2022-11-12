# books/models.py
import uuid  # new
from django.contrib.auth import get_user_model  # new
from django.db import models
from django.urls import reverse


class Book(models.Model):
    id = models.UUIDField(  # new
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # cover = models.ImageField(upload_to="covers/") # new
    cover = models.ImageField(upload_to="covers/", blank=True) # new

    class Meta: # new
        permissions = [
            ("special_status", "Can read all books"),
        ]


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])

"""
The order of the inner classes and methods here is deliberate. It follows the Model stylea
section from the Django documentation
"""

class Review(models.Model):  # new
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    review = models.CharField(max_length=255)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.review

"""
If we wanted to allow uploads of a regular file rather than an image file the only difference
could be to change ImageField to FileField.
"""