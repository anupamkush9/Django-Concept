from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMultiAlternatives

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
    3. Select_related uses inner joins for query optimization.
    4. e.g : 
        SELECT "conceptapp_book"."id",
            "conceptapp_book"."title",
            "conceptapp_book"."author_id",
            "conceptapp_author"."id",
            "conceptapp_author"."name",
            "conceptapp_author"."address"
        FROM "conceptapp_book"
        INNER JOIN "conceptapp_author"
            ON ("conceptapp_book"."author_id" = "conceptapp_author"."id")
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

def twodatabases(request):
    # This line is same as writing Book.objects.using('default').all()
    default_db_books = Book.objects.all()
    read_db_books = Book.objects.using('read_db').all()
    return render(request, 'conceptapp/twodatabases.html', {'default_db_books': default_db_books, 'read_db_books': read_db_books})


def send_mail_view(request):
    """
    Implementation Ref : https://www.geeksforgeeks.org/setup-sending-email-in-django-project/
    """
    context = {}
    if request.method == 'POST':
        address = request.POST.get('address')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if address and subject and message:
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
                context['result'] = 'Email sent successfully'
            except Exception as e:
                context['result'] = f'Error sending email: {e}'
        else:
            context['result'] = 'All fields are required'
    
    return render(request, "conceptapp/email_index.html", context)


def send_email_with_static_image_view(request):
    context = {}
    if request.method == 'POST':
        address = request.POST.get('address')
        current_site = get_current_site(request).domain        
        abs_url = "http://" + current_site +"/email-verify/" + "random_token_value"
        context = {"first_name":"first_name","last_name":"last_name","link":abs_url,
                   "facebook_logo_url" : f"https://static.vecteezy.com/system/resources/previews/018/930/698/non_2x/facebook-logo-facebook-icon-transparent-free-png.png",
                    "twitter_logo_url" : f"https://img.freepik.com/premium-vector/twitter-new-x-logo-design-vector_1340851-70.jpg",
                    "instagram_logo_url" : f"https://img.freepik.com/premium-vector/instagram-vector-logo-icon-social-media-logotype_901408-395.jpg",
                    "my_dummy_logo_url" : f"https://anupamstationery.com/wp-content/uploads/2021/04/Anupam_Logo-400-Width.png",
                }
        # returns html file data same to same with html tags.
        html_message_for_user = render_to_string('conceptapp/verification_email.html', context)
        #remove html tags and returns just the message
        plain_message_for_user = strip_tags(html_message_for_user)
        final_message_for_user = EmailMultiAlternatives('Email Verification', plain_message_for_user, settings.EMAIL_HOST_USER,[address])
        final_message_for_user.attach_alternative(html_message_for_user, 'text/html')
        mail_response = final_message_for_user.send()
    return render(request, "conceptapp/email_index.html", context)
    # return render(request, "conceptapp/verification_email.html", context)