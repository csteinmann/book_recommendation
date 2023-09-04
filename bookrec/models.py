from django.db import models


# Create your models here.
class Book(models.Model):
    book_id = models.IntegerField(unique=True)
    title_without_series = models.CharField(max_length=128)
    book_description = models.CharField(max_length=3000)
    publication_year = models.CharField(max_length=128)
    publisher = models.CharField(max_length=128)
    book_average_rating = models.FloatField(null=True)
    cover_page = models.URLField(max_length=200)
    book_url = models.URLField(max_length=200)

    def __str__(self):
        return self.title_without_series
