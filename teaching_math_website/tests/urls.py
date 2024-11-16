from django.urls import path
from . import views

app_name = 'tests'

urlpatterns = [
    path('', views.tests_list, name='tests_list'),
    path('<int:test_id>/', views.test_detail, name='test_detail'),
    path('<int:test_id>/submit/', views.submit_test, name='submit_test'),
]
