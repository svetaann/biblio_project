from django.contrib import admin
from django.urls import include, path, re_path
# from hello import views
from book import views
urlpatterns = [
    path('favourites/', views.edit_favourites),
    path("review/", views.add_review),
    path("reader/<int:id>/", views.get_profile_info),
    path("reader/", views.create_reader),
    path("book/<int:id>/", views.get_book_by_id),
    path("test/", views.test),
    path("books", views.get_filtered_books),
    path("", views.index),

    # path("create/", views.create),
    # path("edit/<int:id>/", views.edit),
    # path("delete/<int:id>/", views.delete),
]
