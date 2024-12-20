import datetime
from itertools import chain
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Avg, Min, Max, Sum, Q
from django.views.decorators.csrf import csrf_exempt
from book.models import Book, Creator, Favourites, Operation, Reader, Review
from django.db.models.query import Prefetch

def index(request):
    return JsonResponse({})

def get_filtered_books(request):
    title = request.GET.get("title","")
    sortType = request.GET.get("sortType","")
    genre = request.GET.get("genre","")
    fromYear = request.GET.get("fromYear",0)
    toYear = request.GET.get("toYear",0)
    avail = request.GET.get("avail",False)
    highRate = request.GET.get("highRate",False)
    books = Book.objects.all()
    if title != "":
        books = books.filter(title__icontains=title)
    if genre != "":
        books = books.filter(genre=genre)
    if fromYear != 0 :
        books = books.filter(year__gt=fromYear)
    if toYear != 0 :
        books = books.filter(year__lt=toYear)
    if avail:
        books = books.filter(number__gt=0)
    if sortType == "title":
        books = books.order_by("title")
    elif sortType == "author":
        books = books.order_by("author")
    if highRate:
        book_list = []
        for book in books.all():
            rating = Review.objects.filter(book=book).aggregate(Avg("rating"))['rating__avg']
            if rating is not None:
                if float(rating) > 4:
                    book_list.append(book)
        books = Book.objects.none()
        books = list(chain(books, book_list))
    payload = []
    for book in books:
        rating = Review.objects.filter(book=book).aggregate(Avg("rating"))['rating__avg']
        payload.append({"title":book.title, 
                           "author":book.author,
                           "rating":rating})
    return JsonResponse(payload, safe=False, json_dumps_params={'ensure_ascii': False})

def get_book_by_id(request, id):
    book = Book.objects.get(id=id)
    reviews = Review.objects.filter(book=book)
    rating = Review.objects.filter(book=book).aggregate(Avg("rating"))['rating__avg']
    review_list = []
    for review in reviews:
        review_list.append({"name":review.reader.name,
                            "rating":review.rating,  
                            "date":review.date,
                            "text":review.text})
    book_json = {"title":book.title, 
                "author":book.author,
                "year":book.year,
                "genre":book.genre,
                "description":book.description,
                "url":book.url,
                "number":book.number,
                "rating":rating,
                "reviews":review_list}
    return JsonResponse(book_json, json_dumps_params={'ensure_ascii': False})

def get_profile_info(request, id):
    reader = Reader.objects.get(id=id)
    favourites = Favourites.objects.filter(reader=reader).order_by("date")
    favourites_list = []
    for el in favourites:
        favourites_list.append({"title":el.book.title,
                                "author":el.book.author})
    operations = Operation.objects.filter(reader=reader).order_by("date")
    operation_list = []
    for operation in operations:
        operation_list.append({"date":operation.date,
                               "title":operation.book.title,
                               "status":operation.status})
    payload = {"name":reader.name,
                   "email":reader.email,
                   "favourites":favourites_list,
                   "history":operation_list
    }
    return JsonResponse(payload, json_dumps_params={'ensure_ascii': False})

@csrf_exempt 
def create_reader(request):
    body = json.loads(request.body.decode('utf-8'))
    reader = Reader()
    reader.name = body["surname"] + ' ' + body["name"]
    reader.email = body["email"]
    reader.login = body["login"]
    reader.password = body["password"]
    reader.birth_date = body["birth_date"]
    reader.save()
    return JsonResponse({})

@csrf_exempt 
def add_review(request):
    body = json.loads(request.body.decode('utf-8'))
    reader = Reader.objects.get(id=body["reader_id"])
    book = Book.objects.get(id=body["book_id"])
    if Review.objects.filter(reader=reader, book=book).count() == 0:
        review = Review()
        review.reader = reader
        review.book = book
        review.rating = body["rating"]
        if "text" in body.keys():
            review.text = body["text"]
        review.date = body["date"]
        review.save()
    else:
        review = Review.objects.get(reader=reader, book=book)
        review.reader = reader
        review.book = book
        review.rating = body["rating"]
        if "text" in body.keys():
            review.text = body["text"]
        review.date = body["date"]
        review.save()
    return JsonResponse({})

@csrf_exempt 
def edit_favourites(request):
    body = json.loads(request.body.decode('utf-8'))
    reader = Reader.objects.get(id=body["reader_id"])
    book = Book.objects.get(id=body["book_id"])
    if Favourites.objects.filter(reader=reader, book=book).count() == 0:
        favourites = Favourites()
        favourites.reader = reader
        favourites.book = book
        favourites.date = body["date"]
        favourites.save()
    else:
        favourites = Favourites.objects.get(reader=reader, book=book)
        favourites.delete()
    return JsonResponse({})

def books_to_return(request, id):
    reader = Reader.objects.get(id=id)
    operations = Operation.objects.filter(reader=reader).exclude(status="Возвращено")
    playload = []
    for operation in operations:
        playload.append({"date":operation.date,
                        "title":operation.book.title,
                        "status":operation.status})
    return JsonResponse(playload, safe=False)

@csrf_exempt 
def return_book(request, id, book_id):
    reader = Reader.objects.get(id=id)
    book = Book.objects.get(id=book_id)
    operation = Operation.objects.get(reader=reader, book=book)
    operation.status = "Возвращено"
    operation.save()
    return JsonResponse({"id":operation.id})

@csrf_exempt 
def borrow_book(request, id):
    body = json.loads(request.body.decode('utf-8'))
    reader = Reader.objects.get(id=body["id"])
    book = Book.objects.get(id=id)
    if Operation.objects.filter(reader=reader, book=book).count() == 0:
        operation = Operation()
        operation.reader = reader
        operation.book = book
        operation.date = datetime.datetime.now()
        end_date = (datetime.datetime.now() + datetime.timedelta(weeks=4)).strftime('%d.%m.%Y')
        operation.status = f"На руках до {end_date}"
        operation.save()
    return JsonResponse({})

def test(request):
    # reader = Reader()
    # reader.name = "Анненкова Светлана"
    # reader.email = "sveta@ya.ru"
    # reader.login = "sveta123"
    # reader.password = "qwerty12345"
    # reader.birth_date = '2004-04-20'
    # reader.save()
    # reader = Reader()
    # reader.name = "Ильин Федор"
    # reader.email = "ifedor@mail.ru"
    # reader.login = "fedor_22"
    # reader.password = "pass123"
    # reader.birth_date = '2002-01-10'
    # reader.save()
    # reader = Reader()
    # reader.name = "Ромашкин Роман"
    # reader.email = "rom@gmail.ru"
    # reader.login = "romash"
    # reader.password = "11223344"
    # reader.birth_date = '1993-11-01'
    # reader.save()

    # reader = Creator()
    # reader.name = "Иванова Лилия"
    # reader.email = "ivanoval@ya.ru"
    # reader.login = "liliaI"
    # reader.password = "пароль"
    # reader.birth_date = '1850-09-03'
    # reader.save()

    # book = Book()
    # book.title = "Яма"
    # book.author = "Куприн Александр Иванович"
    # book.year = "2022"
    # book.genre = "Классическая проза"
    # book.url = "https://sun9-78.userapi.com/impg/0DLhSbOu0VN3p7g48PbQrgaPL9B_HovPELc-VQ/icjH35ei6YE.jpg?size=690x1080&quality=95&sign=b3dd06966ffed9a7e531d718be109378&type=album"
    # book.description = "Самое трагическое произведение Куприна, которое в свое время произвело среди читателей и критиков эффект разорвавшейся бомбы"
    # book.number = "6"
    # book.creator = Creator.objects.get(id=1)
    # book.save()
    # book = Book()
    # book.title = "Этюд в багровых тонах"
    # book.author = "Артур Конан Дойл"
    # book.year = "2024"
    # book.genre = "Детектив"
    # book.url = "https://sun9-29.userapi.com/impg/fJA6ngHheABBYNKSwYXfOaRganFghR-qKal0JA/q3uScRB4Tkw.jpg?size=480x606&quality=95&sign=51b9e0aa0d70097f44f0df5e53045af6&type=album"
    # book.description = "Первая повесть детективного цикла. Англия, XIX век. Бывший военный врач Джон Уотсон, выйдя в отставку, возвращается в Лондон, где знакомится с загадочным мистером Шерлоком Холмсом - большим специалистом по расследованию таинственных преступлений. Так начинается их первое совместное дело. Проницательный и остроумный Шерлок догадывается, кто стоит за убийством в заброшенном доме, и находит преступника. Трагическая история этого человека переносит читателя в штат Юта на Диком Западе - настоящий оплот мормонов. Книга проиллюстрирована художником Олегом Пахомовым."
    # book.number = "2"
    # book.creator = Creator.objects.get(id=1)
    # book.save()
    # book = Book()
    # book.title = "Оно"
    # book.author = "Стивен Кинг"
    # book.year = "2010"
    # book.genre = "Ужасы"
    # book.url = "https://sun9-19.userapi.com/impg/DIo05lRt_xfhs5O7M-UgBAgnocNDvXNgvoN_gA/xb9vFIX-YHQ.jpg?size=442x692&quality=95&sign=ed48a2f94c7c0a3eacdba9a84bda708b&type=album"
    # book.description = "Одна из самых известных книг Стивена Кинга — теперь и в одной из самых популярных серий на российском книжном рынке."
    # book.number = "3"
    # book.creator = Creator.objects.get(id=1)
    # book.save()
    # book = Book()
    # book.title = "Собачье сердце"
    # book.author = "Булгаков Михаил Афанасьевич"
    # book.year = "2019"
    # book.genre = "Классическая проза"
    # book.url = "https://sun9-11.userapi.com/impg/H0MR6PnTvgciI_Lm8VVmCyWyvcnS1LiOZ256Kg/DQlmGT30IR8.jpg?size=442x692&quality=95&sign=239f1b4deeda28e0bf0a9f162a220f1b&type=album"
    # book.description = "«Собачье сердце», гениальная повесть Михаила Булгакова, написанная еще в 1925 году, едва не стоившая автору свободы и до 1987 года издававшаяся лишь за рубежом и ходившая по рукам в самиздате, в представлениях не нуждается."
    # book.number = "3"
    # book.creator = Creator.objects.get(id=1)
    # book.save()

    # review = Review()
    # review.book = Book.objects.get(id=4)
    # review.reader = Reader.objects.get(id=1)
    # review.rating = 5
    # review.date = '2024-09-07'
    # review.save()
    # review = Review()
    # review.book = Book.objects.get(id=4)
    # review.reader = Reader.objects.get(id=2)
    # review.rating = 4
    # review.text = "Необычное произведение, которое подойдет любителям медицинской тематики, экспериментов и как мне кажется психологии. Мне понравилось повествование некоторых мыслей и историй от лица собаки. В целом моральная составляющая и сюжет хороший. Интересная задумка и подача. Но для меня некоторые моменты оказались достаточно жестокими..."
    # review.date = '2024-10-07'
    # review.save()
    # review = Review()
    # review.book = Book.objects.get(id=1)
    # review.reader = Reader.objects.get(id=2)
    # review.rating = 5
    # review.text = "Определено одна из лучших книг, которые я когда-либо читал. Куприн - гений. Все здесь на высшем уровне - сюжет, персонажи, характеры, судьбы, эмоции, переживания."
    # review.date = '2024-10-22'
    # review.save()
    # review = Review()
    # review.book = Book.objects.get(id=2)
    # review.reader = Reader.objects.get(id=2)
    # review.rating = 3
    # review.date = '2024-07-22'
    # review.save()

    # operation = Operation()
    # operation.book = Book.objects.get(id=4)
    # operation.reader = Reader.objects.get(id=1)
    # operation.date = "2024-08-20"
    # operation.status = "Возвращено"
    # operation.save()
    # operation = Operation()
    # operation.book = Book.objects.get(id=4)
    # operation.reader = Reader.objects.get(id=2)
    # operation.date = "2024-10-01"
    # operation.status = "Возвращено"
    # operation.save()
    # operation = Operation()
    # operation.book = Book.objects.get(id=2)
    # operation.reader = Reader.objects.get(id=2)
    # operation.date = "2024-01-01"
    # operation.status = "Просрочено"
    # operation.save()
    # operation = Operation()
    # operation.book = Book.objects.get(id=1)
    # operation.reader = Reader.objects.get(id=2)
    # operation.date = "2024-10-20"
    # operation.status = "На руках до 20.12.2024"
    # operation.save()

    # favourites = Favourites()
    # favourites.book = Book.objects.get(id=1)
    # favourites.reader = Reader.objects.get(id=2)
    # favourites.date = "2024-06-07"
    # favourites.save()
    # favourites = Favourites()
    # favourites.book = Book.objects.get(id=2)
    # favourites.reader = Reader.objects.get(id=2)
    # favourites.date = "2024-06-07"
    # favourites.save()
    # favourites = Favourites(book=Book.objects.get(id=3), reader=Reader.objects.get(id=2),date="2024-06-07")
    # favourites.save()

    


    return JsonResponse({}, safe=False, json_dumps_params={'ensure_ascii': False})
