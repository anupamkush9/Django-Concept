from django.urls import path
from .views import book_list_select_related, book_list_prefetch_related, book_list_forloop, twodatabases
from .views import index_view, send_mail_view, send_email_with_static_image_view

urlpatterns = [
    path('', index_view),
    path('select_related/', book_list_select_related, name='select_related'),
    path('prefetch_related/', book_list_prefetch_related, name='prefetch_related'),
    path('forloop/', book_list_forloop, name='forloop'),
    path('twodatabases/', twodatabases, name='twodatabases'),
    path('send_mail_view/', send_mail_view, name="send_mail_view"),
    path('send_email_with_static_image/', send_email_with_static_image_view, name="send_email_with_static_image_view")
]
