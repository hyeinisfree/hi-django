from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:year>/', views.index, name='index'),
    path('<int:year>/<int:homework_id>/detail/', views.detail, name='detail'),
    path('<int:year>/<int:homework_id>/submit/', views.submit, name='submit'),
    path('<int:year>/<int:homework_id>/result/', views.result, name='result')
]