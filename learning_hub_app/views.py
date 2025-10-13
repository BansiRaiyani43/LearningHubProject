from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
# from django.shortcuts import render
# from .models import User
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

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("signup")

        # ----------------- Create User -----------------
        user = User.objects.create_user(
            username=username,
            email=email,
            phone_no=phone_no or None,
            role=role,
            password=password1
        )

        login(request, user)  # auto-login
        messages.success(request, f"Registration successful! Welcome {user.username}.")

        # ----------------- Redirect Based on Role -----------------
        if role == "student":
            return redirect("index")
        elif role == "teacher":
            return redirect("index")
        else:
            return redirect("login")

    return render(request, "sign_up.html")







# ------------------ LOGIN VIEW ------------------
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on role
            if user.role == "student":
                return redirect("index")
            elif user.role == "teacher":
                return redirect("index")
            elif user.role == "admin":
                return redirect("index")
            else:
                messages.error(request, "Invalid role assigned.")
                return redirect("login")

        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "index.html")

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
    return render(request, "index.html")

@login_required
def admin_dashboard(request):
    return render(request, "index.html")











# Create your views here.
def BASE(request):
    return render(request, 'index.html')

def sign_up(request):
    return render(request, 'sign_up.html')

def sign_in(request):
    return render(request, 'sign_in.html')