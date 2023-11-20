from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests

from .forms import MainBooksForm
from .models import MainBooks, Category, Framework

api_key = 'AIzaSyCTm9EWtvOvEtiRIlnIH5sH0XETPz8Mf3A'
query = "java"


@login_required(login_url='login')
def home(request):
    books_data = fetch_books_data(request)
    main_books_data = main_books(request)
    framework = frameworks(request)
    category = categories(request)
    book1 = []
    book2 = []
    book3 = []
    i = 0
    for book in main_books_data:
        if i < 3 and book.type == "free":
            book1.append(book)
        elif i < 5 and book.type == "free":
            book2.append(book)
        else:
            book3.append(book)
        i += 1

    context = {
        "books": books_data,
        "books2": book2,
        "main_books": book1,
        "category": category,
        "framework": framework,
        "book3": book3
    }

    return render(request, 'library/index.html', context)


@login_required(login_url='login')
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
                "bookinfo": book.get('id', ''),
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


import requests


@login_required(login_url='login')
def book_description(request, description):
    base_url = 'https://www.googleapis.com/books/v1/volumes'
    params = {'q': description}

    response = requests.get(base_url, params=params)
    datainfo = []
    if response.status_code == 200:
        data = response.json()
        if 'items' in data:
            first_item = data['items'][0]['volumeInfo']
            datainfo.append({
                "title": first_item.get('title', 'N/A'),
                "description": first_item.get('description', 'N/A'),
                "authors": first_item.get('authors', ['N/A']),
                "date_published": first_item.get('publishedDate', 'N/A'),
                "pdf_link": first_item.get('pdfLink', 'Not Available'),
                "is_for_sale": first_item.get('saleInfo', {}).get('saleability', 'Not Available'),
                "image_link": first_item.get('imageLinks', {}).get('thumbnail', 'Not Available'),
                "page_count": first_item.get('pageCount', 'N/A')
            })

    return render(request, 'library/book_description.html', {"bookinfo": datainfo})


@login_required(login_url='login')
def bookupload(request):
    if request.method == 'POST':
        form = MainBooksForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user.is_authenticated:
                category_name = form.cleaned_data['category']
                topic, created = Category.objects.get_or_create(category_name=category_name)
                MainBooks.objects.create(
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    topic=topic,
                    auther=request.user.username,
                    image=form.cleaned_data['image'],
                    book=form.cleaned_data['book'],
                    type=form.cleaned_data['type'],
                    amount=form.cleaned_data['amount'],
                    category=form.cleaned_data['category'],
                )
                return redirect('libraryhome')
            else:
                return render(request, 'socialmedia/login_register.html')
        else:
            print("Form is not valid. Please check the form data.")
    else:
        form = MainBooksForm()
    context = {'form': form}
    return render(request, 'library/fileUpload.html', context)