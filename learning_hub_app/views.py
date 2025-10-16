from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone_no")
        role = request.POST.get("role")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # ----------------- Validation -----------------
        if not username or not email or not password1 or not password2 or not role:
            messages.error(request, "Please fill in all required fields.")
            return redirect("signup")

        elif password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        else:    
            user = User.objects.create_user(
            username=username,
            email=email,
            phone_no=phone_no,  
            role=role,
            password=password1
          )
            user.save()

            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
    return render(request, 'sign_up.html')
        
# ------------------ LOGIN VIEW ------------------
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("DEBUG → username:", username, "password:", password)


        user = authenticate(request, username=username, password=password)
        print("DEBUG → user:", user)


        if user is not None:
            if not user.is_active:
                messages.error(request, "Your account is inactive")
                return redirect("login")
            login(request, user)
            print("DEBUG → user.role:", user.role)


            # Redirect based on role
            if user.role == "student":
                return redirect("student_dashboard")
            elif user.role == "teacher":
                print("Redirecting to teacher dashboard")
                return redirect("teacher_dashboard")
            elif user.role == "admin":
                return redirect("admin_dashboard")
            else:
                messages.error(request, "Invalid role assigned.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "login.html")

# ------------------ LOGOUT VIEW ------------------
def user_logout(request):
    logout(request)
    return redirect("login")

# ------------------ DASHBOARD VIEWS ------------------
@login_required
def student_dashboard(request):
    return render(request, "index.html")

@login_required
def teacher_dashboard(request): 
    return render(request, "teacher/teacher_dashboard.html")

@login_required
def admin_dashboard(request):
    return render(request, "index.html")











# Create your views here.
def BASE(request):
    return render(request, 'index.html')

def BASET(request):
    return render(request, 'teacher/index.html')

def sign_up(request):
    return render(request, 'sign_up.html')

def sign_in(request):
    return render(request, 'sign_in.html')