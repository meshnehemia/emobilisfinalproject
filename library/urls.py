from django.urls import path
from library import views

urlpatterns = [
    path('', views.home, name='libraryhome'),
    path('uploadfile/', views.bookupload, name='newBook'),
    path('editfile/<int:pk>', views.edit_book, name='editbook'),
    path('description/<str:description>', views.book_description, name='describebook'),
    path('available/<str:pk>', views.mainbookinformation, name='MainbookDescription'),
    path('buy/<str:pk>', views.buybook, name='buybook'),
]
