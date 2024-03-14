from django.urls import path
from .views import book_list_select_related, book_list_prefetch_related, book_list_forloop
from .views import index_view

urlpatterns = [
    path('', index_view),
    path('select_related/', book_list_select_related, name='select_related'),
    path('prefetch_related/', book_list_prefetch_related, name='prefetch_related'),
    path('forloop/', book_list_forloop, name='forloop'),
]
