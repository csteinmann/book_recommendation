from django.urls import path
from bookrec import views

app_name = 'bookrec_app'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('survey/thank-you/', views.thank_you_view, name='thank_you'),
    path('survey/', views.survey_view, name='survey'),
    path('log_button_click/', views.log_button_click, name='log_button_click'),
]
