from django.shortcuts import render
from .models import User

# Create your views here.
def BASE(request):
    return render(request, 'index.html')

def sign_up(request):
    return render(request, 'sign_up.html')

def sign_in(request):
    return render(request, 'sign_in.html')