from django.urls import path
from bookrec import views

app_name = 'bookrec_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('thank-you/', views.thank_you_view, name='thank_you')
]
