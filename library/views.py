from django.shortcuts import render
import requests
from .models import MainBooks, Category, Framework

api_key = 'AIzaSyCTm9EWtvOvEtiRIlnIH5sH0XETPz8Mf3A'
query = "java"


def home(request):
    books_data = fetch_books_data(request)
    main_books_data = main_books(request)
    framework = frameworks(request)
    category = categories(request)
    book1 = []
    book2 = []
    i = 0
    for book in main_books_data:
        if i < 3:
            book1.append(book)
        elif i < 5:
            book2.append(book)
        else:
            break
        i += 1

    context = {
        "books": books_data,
        "books2": book2,
        "main_books": book1,
        "category": category,
        "framework": framework
    }

    return render(request, 'library/index.html', context)


def fetch_books_data(request):
    base_url = 'https://www.googleapis.com/books/v1/volumes'
    params = {
        'q': query,
        'key': api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        books = []
        for book in response.json().get('items', []):
            books.append({
                "bookinfo": book.get('selfLink', ''),
                "title": book['volumeInfo'].get('title', ''),
                "image": book['volumeInfo']['imageLinks'].get('thumbnail', ''),
            })

        return books
    except requests.exceptions.RequestException as e:
        print(e)


def main_books(request):
    books = MainBooks.objects.all().order_by('-updated_at')
    return books


def categories(request):
    category = Category.objects.all().order_by('-updated_at')
    return category


def frameworks(request):
    framework = Framework.objects.all().order_by('-updated_at')
    return framework
