from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages

User = get_user_model()


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')

        if password != password_confirmation:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('register')

        # Yangi foydalanuvchi yaratish
        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('categories_home')
        else:
            messages.error(request, "Invalid email or password.")

    next_url = request.GET.get('next')  # GET so'rovdan 'next' qiymatini olish
    return render(request, 'login.html', {'next': next_url})


def user_logout(request):
    logout(request)  # Foydalanuvchini tizimdan chiqarish
    return redirect('categories_home')  # Categories sahifasiga yo'naltirish


def account_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")

        # Ma'lumotlarni yangilash
        user = request.user
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email

        # Parolni tekshirish va yangilash
        if password:
            if password == password_confirmation:
                user.set_password(password)
            else:
                messages.error(request, "Passwords do not match.")
                return redirect("account")

        user.save()
        messages.success(request, "Your account information has been updated.")
        return redirect("account")

    return render(request, "account.html")