from django.urls import path
from bookrec import views

app_name = 'bookrec_app'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('survey/thank-you/', views.thank_you_view, name='thank_you'),
    path('survey/', views.survey_view, name='survey'),
    path('logging/', views.logging_view, name='logging'),
]
