from django.db import models
from django.contrib.auth.models import User


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
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.question.text}:{self.text}"


class SurveyResponse(models.Model):
    AGE_GROUP_CHOICES = [
        ('Under 18', 'Under 18'),
        ('18-24', '18-24'),
        ('25-34', '25-34'),
        ('35-44', '35-44'),
        ('45-54', '45-54'),
        ('55-64', '55-64'),
        ('Above 64', 'Above 64'),
        ('I prefer not to say', 'I prefer not to say')
    ]

    GENDER_CHOICES = [
        ('Woman', 'Woman'),
        ('Man', 'Man'),
        ('Non-binary', 'Non-binary'),
        ('I prefer not to say', 'I prefer not to say'),
    ]

    READING_PLATFORM_CHOICES = [
        ('Physical books', 'Physical books'),
        ('E-books', 'E-books'),
        ('Audiobooks', 'Audiobooks'),
        ('Online articles', 'Online articles'),
        ('Other', 'Other'),
    ]

    BOOK_FREQUENCY_CHOICES = [
        ('0-4', '0-4'),
        ('5-9', '5-9'),
        ('10-14', '10-14'),
        ('15-10', '15-20'),
        ('More than 20', 'More than 20')
    ]

    GENRE_CHOICES = [
        ('Mystery, thriller and crime', 'Mystery, thriller and crime'),
        ('History', 'History'),
        ('Biographies', 'Biographies'),
        ('Romance', 'Romance'),
        ('Cookbooks', 'Cookbooks'),
        ('Science fiction', 'Science fiction'),
        ('Fantasy', 'Fantasy'),
        ('Classics/literature', 'Classics/literature'),
        ('Health', 'Health'),
        ('Religion/spirituality', 'Religion/spirituality'),
        ('Self-help', 'Self-help'),
        ('True crime', 'True crime'),
        ('Political', 'Political'),
        ('Business', 'Business'),
        ('Poetry', 'Poetry'),
        ('Westerns', 'Westerns'),
        ('Other fiction', 'Other fiction'),
        ('Other non-fiction', 'Other non-fiction'),
        ('None', 'None'),
    ]

    survey = models.ForeignKey(Survey, on_delete=models.PROTECT)
    sessionId = models.CharField(max_length=128)
    rotation_state = models.CharField(max_length=128)
    answer = models.ManyToManyField(Choice)
    age_group = models.CharField(max_length=128)
    gender = models.CharField(max_length=512)
    reading_platform = models.CharField(max_length=128)
    book_frequency = models.CharField(max_length=128)
    genre = models.CharField(max_length=8192)

    def __str__(self):
        return f"{self.sessionId}:{self.rotation_state}"
