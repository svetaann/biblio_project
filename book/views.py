from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Avg, Min, Max, Sum
from django.views.decorators.csrf import csrf_exempt
from book.models import Book, Favourites, Operation, Reader, Review

def get_books(request):
    books = Book.objects.all()
    books_list = []
    for book in books:
        books_list.append({"title":book.title, 
                           "author":book.author,
                           "year":book.year,
                           "genre":book.genre,
                           "description":book.description,
                           "creator":book.creator.name})
    return JsonResponse(books_list, safe=False)

def get_book_by_id(request, id):
    book = Book.objects.get(id=id)
    reviews = Review.objects.filter(book=book)
    rating = Review.objects.filter(book=book).aggregate(Avg("rating"))['rating__avg']
    review_list = []
    for review in reviews:
        review_list.append({"rating":review.rating, 
                            "text":review.text, 
                            "date":review.date, 
                            "reader":review.reader.name})
    book_json = {"title":book.title, 
                "author":book.author,
                "year":book.year,
                "genre":book.genre,
                "description":book.description,
                "url":book.url,
                "number":book.number,
                "creator":book.creator.name,
                "rating":rating,
                "reviews":review_list}
    return JsonResponse(book_json)

def get_profile_info(request, id):
    reader = Reader.objects.get(id=id)
    favourites = Favourites.objects.filter(reader=reader)
    favourites_list = []
    for el in favourites:
        favourites_list.append({"title":el.book.title,
                                "author":el.book.author,
                                "year":el.book.year})
    operations = Operation.objects.filter(reader=reader)
    operation_list = []
    for operation in operations:
        operation_list.append({"date":operation.date,
                               "title":operation.book.title,
                               "status":operation.status})
    reader_json = {"name":reader.name,
                   "email":reader.email,
                   "favourites":favourites_list,
                   "history":operation_list
    }
    return JsonResponse(reader_json)


@csrf_exempt
def get_books_by_title(request):
    return request.POST.get("title")

# # получение данных из бд
# def index(request):
#     products = Product.objects.all()
#     return render(request, "index.html", {"products": products})
 
# # добавление данных из бд
# def create(request):
#     create_companies()  # добавляем начальные данные для компаний
 
#     # если запрос POST, сохраняем данные
#     if request.method == "POST":
#         product = Product()
#         product.name = request.POST.get("name")
#         product.price = request.POST.get("price")
#         product.company_id = request.POST.get("company")
#         product.save()
#         return HttpResponseRedirect("/")
#     # передаем данные в шаблон
#     companies = Company.objects.all()
#     return render(request, "create.html", {"companies": companies})
 
# # изменение данных в бд
# def edit(request, id):
#     try:
#         product = Product.objects.get(id=id)
 
#         if request.method == "POST":
#             product.name = request.POST.get("name")
#             product.price = request.POST.get("price")
#             product.company_id = request.POST.get("company")
#             product.save()
#             return HttpResponseRedirect("/")
#         else:
#             companies = Company.objects.all()
#             return render(request, "edit.html", {"product": product, "companies": companies})
#     except Product.DoesNotExist:
#         return HttpResponseNotFound("<h2>Product not found</h2>")
     
# # удаление данных из бд
# def delete(request, id):
#     try:
#         product = Product.objects.get(id=id)
#         product.delete()
#         return HttpResponseRedirect("/")
#     except Product.DoesNotExist:
#         return HttpResponseNotFound("<h2>Product not found</h2>")
 
# # добавление начальных данных в таблицу компаний
# def create_companies():
      
#      if Company.objects.all().count() == 0:
#           Company.objects.create(name = "Apple")
#           Company.objects.create(name = "Asus")
#           Company.objects.create(name = "MSI")