from django.contrib import admin
from bookrec.models import Book, Survey, Question, Choice, Submission


class BookAdmin(admin.ModelAdmin):
    search_fields = ['title_without_series', 'book_id']


# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Submission)
