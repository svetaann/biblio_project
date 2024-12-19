from django.contrib import admin
from django.urls import include, path, re_path
# from hello import views
from book import views
urlpatterns = [
    
    path("reader/<int:id>/", views.get_profile_info),
    path("book/<int:id>/", views.get_book_by_id),
    path("book/", views.get_books_by_title),
    path("", views.get_books),

#     path("create/", views.create),
#     path("edit/<int:id>/", views.edit),
#     path("delete/<int:id>/", views.delete),
]