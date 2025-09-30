from django.shortcuts import render
from .models import User

# Create your views here.
def BASE(request):
    return render(request, 'home.html')