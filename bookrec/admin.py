from django.contrib import admin
from bookrec.models import Book, Survey, Question, Choice, SurveyResponse, RotationState


class BookAdmin(admin.ModelAdmin):
    search_fields = ['title_without_series', 'book_id']


class QuestionInLine(admin.TabularInline):
    model = Question
    show_change_link = True


class ChoiceInLine(admin.TabularInline):
    model = Choice


class SurveyAdmin(admin.ModelAdmin):
    inlines = [QuestionInLine]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLine]


# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(SurveyResponse)
admin.site.register(RotationState)
