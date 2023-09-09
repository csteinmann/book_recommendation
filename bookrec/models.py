from django.db import models


# Create your models here.
class Book(models.Model):
    book_id = models.IntegerField(unique=True)
    title_without_series = models.CharField(max_length=128)
    book_description = models.CharField(max_length=6000)
    publication_year = models.CharField(max_length=128)
    publisher = models.CharField(max_length=128)
    book_average_rating = models.FloatField(null=True)
    cover_page = models.URLField(max_length=200)
    book_url = models.URLField(max_length=200)

    def __str__(self):
        return self.title_without_series


class Survey(models.Model):
    title = models.CharField(max_length=128)
    rotation_state = models.CharField(unique=True, max_length=128)

    def __str__(self):
        return self.title


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.question.text}:{self.text}"


class Submission(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT)
    answer = models.ManyToManyField(Choice)
    status = models.CharField(max_length=200)