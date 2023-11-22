from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .credentials import MpesaAccessToken, LipanaMpesaPpassword
from .forms import MainBooksForm, CategoryForm
from .models import MainBooks, Category, Framework, BookBought

api_key = 'AIzaSyCTm9EWtvOvEtiRIlnIH5sH0XETPz8Mf3A'
query = "java"
user = ''
search = 'none'


@login_required(login_url='login')
def home(request):
    check = request.GET.get('search', '')
    if request.method == 'GET' and check != '':
        global query
        global search
        query = request.GET.get('search', 'java')
        search = query
    books_data = fetch_books_data(request)
    main_books_data = main_books(request)
    framework = frameworks(request)
    category = categories(request)
    book1 = []
    book2 = []
    book3 = []
    i = 0
    k = 0
    for book in main_books_data:
        if k < 5 and book.type == "free":
            book1.append(book)
            k += 1
        elif k < 5 and book.type == "free":
            book2.append(book)
            k += 1
        else:
            pass
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
            volume_info = book.get('volumeInfo', {})

            books.append({
                "bookinfo": book.get('id', ''),
                "title": volume_info.get('title', ''),
                "image": volume_info.get('imageLinks', {}).get('thumbnail', ''),
            })

        return books
    except requests.exceptions.RequestException as e:
        print(e)


def main_books(request):
    if search == 'none':
        books = MainBooks.objects.all().order_by('-updated_at')
    else:
        books = MainBooks.objects.filter(
            Q(title__icontains=query) |
            Q(auther__name__contains=query) |
            Q(auther__username__contains=query) |
            Q(auther__email__contains=query) |
            Q(type__contains=query)
        ).order_by('-updated_at')
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
                    auther=request.user,
                    image=form.cleaned_data['image'],
                    book=form.cleaned_data['book'],
                    type=form.cleaned_data['type'],
                    amount=form.cleaned_data['amount'],
                    category=form.cleaned_data['category'],
                )
                book = MainBooks.objects.get(title=form.cleaned_data['title'], topic=topic,
                                             description=form.cleaned_data['description'], auther=request.user, )
                return mainbookinformation(request, book.pk)
            else:
                return render(request, 'socialmedia/login_register.html')
        else:
            print("Form is not valid. Please check the form data.")
            print(form.errors)
    else:
        form = MainBooksForm()
    context = {'form': form}
    return render(request, 'library/fileUpload.html', context)


def mainbookinformation(request, pk):
    book = MainBooks.objects.get(pk=pk)
    try:
        customer = BookBought.objects.get(customer=request.user, book=book)
    except BookBought.DoesNotExist:
        customer = ''
    context = {"book": book, "customer": customer}
    return render(request, 'library/mainBookDescription.html', context)


def buybook(request, pk):
    book = get_object_or_404(MainBooks, pk=pk)

    if request.method == 'POST':
        phone = request.POST['phone']
        amount = int(book.amount)
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        mpesa_request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": 254757316903,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": f"mesh library username: {request.user.username}: title {book.title}",
            "TransactionDesc": "Web Development Charges"
        }
        requests.post(api_url, json=mpesa_request, headers=headers)
        BookBought.objects.get_or_create(
            book=book,
            customer=request.user,
            amount=amount
        )
        try:
            cm = BookBought.objects.get(customer=request.user, book=book)
        except BookBought.DoesNotExist:
            cm = ''
        context = {"book": book, "customer": cm}
        return render(request, 'library/mainBookDescription.html', context)
    try:
        customer = BookBought.objects.get(customer=request.user, book=book)
    except BookBought.DoesNotExist:
        customer = None
    context = {"book": book, "customer": customer}
    return render(request, 'library/buybook.html', context)


def searchwithcategory(request, ctname):
    global query, search
    query = ctname
    search = ctname
    return home(request)


def addcategory(request):
    category = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return home(request)
    context = {"form": category}
    return render(request, 'library/uploadCategory.html', context)


def deletebook(request, pk):
    try:
        book = MainBooks.objects.get(pk=pk)
        book.delete()
    except MainBooks.DoesNotExist:
        pass

    return home(request)


def edit_book(request, pk):
    book = get_object_or_404(MainBooks, pk=pk)
    if request.method == 'POST':
        form = MainBooksForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book_instance = form.save(commit=False)
            category_name = form.cleaned_data['category'].category_name
            book_instance.topic = category_name
            book_instance.save()
            return mainbookinformation(request, pk)
    else:
        form = MainBooksForm(instance=book)
    context = {'form': form, 'book': book}
    return render(request, 'library/edit_book.html', context)


def checkmytotalsales(request):
    books = MainBooks.objects.filter(auther=request.user)
    getbooks = []

    for book in books:
        try:
            get = BookBought.objects.filter(book_id__gt=book.id)
            for add in get:
                getbooks.append(add)
        except BookBought.DoesNotExist:
            pass

    context = {"books": getbooks}
    return render(request, 'library/bookPayment.html', context)


def checkbooksales(request, title):
    getbooks = BookBought.objects.filter(book__title=title, book__auther=request.user).order_by('-date')
    books = BookBought.objects.all()
    for book in books:
        print(book.book.auther.email)
        print(book.book.title)
    context = {"books": getbooks}
    return render(request, 'library/bookPayment.html', context)


@login_required(login_url='login')
def checkcustomerpurches(request, customer):
    getbooks = BookBought.objects.filter(customer__username=customer, book__auther=request.user).order_by('-date')
    context = {"books": getbooks}
    return render(request, 'library/bookPayment.html', context)
