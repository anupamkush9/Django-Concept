from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import Book

def index_view(request):
    print("====================")
    # import time
    # time.sleep(1)
    # Ref +Django Debug Toolbar
    # https://www.youtube.com/watch?v=c5riXBYFxLk
    return render(request, 'conceptapp/index.html',{"t1":"akshay"})

def book_list_select_related(request):
    '''
    1. Reduces the number of database queries by performing inner joins.
    2. Useful for fetching one-to-many relationships or accessing a single related object.
    '''
    books = Book.objects.select_related('author').all()
    return render(request, 'conceptapp/book_list.html', {'books': books, 'title': 'Books (select_related)'})

def book_list_prefetch_related(request):
    '''
    1. Reduces the number of database queries by performaing inner joins and IN operator.
    2. Useful for fetching many-to-many relationships or accessing multiple related objects.
    '''
    books = Book.objects.prefetch_related('author').all()
    return render(request, 'conceptapp/book_list.html', {'books': books, 'title': 'Books (prefetch_related)'})

def book_list_forloop(request):
    '''
    # prefetch related and select related program.
    # https://www.youtube.com/watch?v=TzgZBg7oXNA     #video link for select related and pre-fetch related program
    '''
    books = Book.objects.all()
    return render(request, 'conceptapp/author_list.html', {'books': books, 'title': 'Authors (Normal Approach)'})


