from django.urls import path
from bookrec import views

app_name = 'bookrec_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('survey/<int:id>/', views.show_survey, name='show-survey'),
]