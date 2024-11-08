from django.urls import path
from . import views

app_name = 'lectures'

urlpatterns = [
    path('', views.lectures_list, name="lectures_list"),
]