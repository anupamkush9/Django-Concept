from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index_view(request):
    print("====================")
    import time
    time.sleep(1)
    return render(request, 'conceptapp/index.html',{"t1":"akshay"})