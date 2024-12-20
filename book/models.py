from django.db import models

class Reader(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    birth_date = models.DateField()
    
class Creator(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    birth_date = models.DateField()

class Book(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    year = models.IntegerField()
    genre = models.CharField(max_length=50)
    url = models.URLField(null=True)
    description = models.TextField(null=True)
    number = models.IntegerField()

class Operation(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=50)

class Favourites(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateField()

class Review(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()
    text = models.TextField(null=True)
    date = models.DateField()