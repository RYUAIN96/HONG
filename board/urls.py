# urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('list', views.list, name="list"),
    path('write', views.write, name="write"),
    path('content', views.content, name="content"),
    path('edit', views.edit, name="edit"),
    path('delete', views.delete, name="delete"),
    path('dataframe', views.dataframe, name="dataframe"),

]
