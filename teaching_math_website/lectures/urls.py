from django.urls import path
from . import views

urlpatterns = [
    path('', views.lectures_list),
]