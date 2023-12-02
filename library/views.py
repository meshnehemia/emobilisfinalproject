from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from socialmedia.models import User
from .credentials import MpesaAccessToken, LipanaMpesaPpassword
from .forms import MainBooksForm, CategoryForm
from .models import MainBooks, Category, Framework, BookBought, UsersPayment
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

api_key = 'AIzaSyCTm9EWtvOvEtiRIlnIH5sH0XETPz8Mf3A'
user = ''


@login_required(login_url='login')
def home(request):
    search = 'python'
    sr = ''
    check = request.GET.get('search', '')
    if request.method == 'GET' and check != '':
        search = request.GET.get('search', 'java')
        sr = search
    books_data = fetch_books_data(request, search)
    main_books_data = main_books(request, sr)
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
        "categories": framework,
        "book3": book3
    }

    return render(request, 'library/index.html', context)


def searchhome(request, search):
    check = request.GET.get('search', '')
    if request.method == 'GET' and check != '':
        search = request.GET.get('search', 'java')
    books_data = fetch_books_data(request, search)
    main_books_data = main_books(request, search)
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
        "categories": framework,
        "book3": book3
    }

    return render(request, 'library/index.html', context)


@login_required(login_url='login')
def fetch_books_data(request, query):
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


def main_books(request, search):
    if search == 'none' or search == '' or search == None:
        books = MainBooks.objects.all().order_by('-updated_at')
    else:
        books = MainBooks.objects.filter(
            Q(title__icontains=search) |
            Q(auther__name__icontains=search) |
            Q(auther__username__icontains=search) |
            Q(auther__email__icontains=search) |
            Q(type__icontains=search) |
            Q(category__category_name__icontains=search) |
            Q(description__icontains=search)
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


@csrf_exempt
@login_required(login_url='login')
def bookupload(request):
    if request.method == 'POST':
        form = MainBooksForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user.is_authenticated:
                book, book_created = MainBooks.objects.get_or_create(
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    topic=form.cleaned_data['topic'],
                    auther=request.user,
                    image=form.cleaned_data['image'],
                    book=form.cleaned_data['book'],
                    type=form.cleaned_data['type'],
                    amount=form.cleaned_data['amount'],
                    category=form.cleaned_data['category'],
                )

                if book_created:
                    # return JsonResponse({'success': True, 'redirect_url': f'/library/mainbookinformation/{book.pk}/'})
                    # return mainbookinformation(request, book.pk)
                    return JsonResponse({'success': 'success'})
                else:
                    return JsonResponse({'success': False, 'error': form.errors})
            else:
                return JsonResponse({'success': False, 'error': form.errors})
        else:
            return JsonResponse({'success': False, 'error': form.errors})
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


# @csrf_exempt
# def buybook(request, pk):
#     book = get_object_or_404(MainBooks, pk=pk)
#
#     if request.method == 'POST':
#         phone = request.POST['phone']
#         amount = int(book.amount)
#         access_token = MpesaAccessToken.validated_mpesa_access_token
#         api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
#         headers = {"Authorization": "Bearer %s" % access_token}
#         mpesa_request = {
#             "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
#             "Password": LipanaMpesaPpassword.decode_password,
#             "Timestamp": LipanaMpesaPpassword.lipa_time,
#             "TransactionType": "CustomerPayBillOnline",
#             "Amount": amount,
#             "PartyA": 254757316903,
#             "PartyB": LipanaMpesaPpassword.Business_short_code,
#             "PhoneNumber": phone,
#             "CallBackURL": "https://musing-fog-55251.pktriot.net/mpesa-callback/",
#             "AccountReference": f"mesh library username: {request.user.username}: title {book.title}",
#             "TransactionDesc": "Web Development Charges"
#         }
#         requests.post(api_url, json=mpesa_request, headers=headers)
#         BookBought.objects.get_or_create(
#             book=book,
#             customer=request.user,
#             amount=amount
#
#         )
#         try:
#             cm = BookBought.objects.get(customer=request.user, book=book)
#         except BookBought.DoesNotExist:
#             cm = ''
#         context = {"book": book, "customer": cm}
#         return render(request, 'library/mainBookDescription.html', context)
#     try:
#         customer = BookBought.objects.get(customer=request.user, book=book)
#     except BookBought.DoesNotExist:
#         customer = None
#     context = {"book": book, "customer": customer}
#     return render(request, 'library/buybook.html', context)
#

@csrf_exempt
def buybook(request, pk):
    book = get_object_or_404(MainBooks, pk=pk)

    context = {"book": book, "customer": None}

    if request.method == 'POST':
        phone = request.POST.get('phone')
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
            "CallBackURL": "https://musing-fog-55251.pktriot.net/library/mpesa-callback/" + pk + "/" + str(
                request.user.pk) + "/",
            "AccountReference": f"mesh library username: {request.user.username}: book title {book.title}",
            "TransactionDesc": "Web Development Charges"
        }

        try:
            # Make the M-Pesa API request
            response = requests.post(api_url, json=mpesa_request, headers=headers)

            # Handle the API response
            if response.status_code == 200:
                # Payment initiation successful
                # You can return a response or render a confirmation page if needed
                return render(request, 'library/payment_initiated.html', {"pk": pk})
            else:
                # Handle API errors
                return HttpResponse(f"Error initiating payment: {response.text}", status=response.status_code)

        except Exception as e:
            # Handle exceptions (e.g., network errors)
            return HttpResponse(f"Exception: {str(e)}", status=500)

    try:
        customer = BookBought.objects.get(customer=request.user, book=book)
        context["customer"] = customer
    except BookBought.DoesNotExist:
        pass

    return render(request, 'library/buybook.html', context)


@csrf_exempt
def mpesa_callback(request, pk, upk):
    if request.method == 'POST':
        try:
            callback_data = json.loads(request.body)
            transaction_status = callback_data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
            print(int(transaction_status))
            if int(transaction_status) == 0:

                amount = \
                    callback_data.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata', {}).get('Item', [])[
                        0].get(
                        'Value', '')
                receipt = \
                    callback_data.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata', {}).get('Item', [])[
                        1].get(
                        'Value', '')
                date = callback_data.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata', {}).get('Item', [])[
                    3].get('Value', '')
                number = \
                    callback_data.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata', {}).get('Item', [])[
                        4].get(
                        'Value', '')

                book = MainBooks.objects.get(pk=pk)
                request.user = User.objects.get(pk=upk)
                BookBought.objects.get_or_create(
                    book=book,
                    customer=request.user,
                    amount=amount,
                    receipt=receipt,
                    number=number
                )
                return HttpResponse(json.dumps({"ResultCode": "0", "ResultDesc": "Success"}),
                                    content_type='application/json')
            else:
                return HttpResponse(json.dumps({"ResultCode": transaction_status, "ResultDesc": "Failed"}),
                                    content_type='application/json')

        except Exception as e:
            # Print the exception for further investigation
            print(f"Exception: {str(e)}")
            return HttpResponse(f"Exception: {str(e)}", status=500)

    return HttpResponse(status=405)


def searchwithcategory(request, ctname):
    return searchhome(request, ctname)


@csrf_exempt
def addcategory(request):
    category = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return home(request)
    context = {"form": category}
    return render(request, 'library/uploadCategory.html', context)


@csrf_exempt
def deletebook(request, pk):
    book = MainBooks.objects.get(pk=pk)
    try:
        if request.method == 'POST':
            book.delete()
            return home(request)
    except MainBooks.DoesNotExist:
        pass
    return render(request, 'library/delete.html', {"obj": book.title})


@csrf_exempt
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


def mybooks(request):
    mybooks = MainBooks.objects.filter(auther=request.user)
    context = {"main_books": mybooks}
    return render(request, 'library/mybooks.html', context)
