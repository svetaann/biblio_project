from django.contrib import admin
from django.urls import include, path, re_path
# from hello import views
from book import views
urlpatterns = [
    path("", views.get_books),
#     path("create/", views.create),
#     path("edit/<int:id>/", views.edit),
#     path("delete/<int:id>/", views.delete),
]