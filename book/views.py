from django.http import JsonResponse
from django.shortcuts import render

from book.models import Book

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