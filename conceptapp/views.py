from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index_view(request):
    print("====================")
    # import time
    # time.sleep(1)
    # Ref +Django Debug Toolbar
    # https://www.youtube.com/watch?v=c5riXBYFxLk
    return render(request, 'conceptapp/index.html',{"t1":"akshay"})