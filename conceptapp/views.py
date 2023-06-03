from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import Book

def index_view(request):
    print("====================")
    import time
    time.sleep(1)
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
    books = Book.objects.all()
    return render(request, 'conceptapp/author_list.html', {'books': books, 'title': 'Authors (Normal Approach)'})

def twodatabases(request):
    # This line is same as writing Book.objects.using('default').all()
    default_db_books = Book.objects.all()
    read_db_books = Book.objects.using('read_db').all()
    return render(request, 'conceptapp/twodatabases.html', {'default_db_books': default_db_books, 'read_db_books': read_db_books})

