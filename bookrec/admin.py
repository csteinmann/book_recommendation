from django.contrib import admin
from bookrec.models import Book, Survey, Question, Choice, Submission


# Register your models here.
admin.site.register(Book)
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Submission)
