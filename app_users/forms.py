from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


def user_login(request):
    """Foydalanuvchini tizimga kiritish."""
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect('categories_home')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'login.html')


def register(request):
    """Foydalanuvchini ro'yxatdan o'tkazish."""
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')

        if password != password_confirmation:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('register')

        # Foydalanuvchini yaratish
        user = User.objects.create_user(
            username=email,  # Django username sifatida emailni saqlash
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')

    return render(request, 'register.html')
