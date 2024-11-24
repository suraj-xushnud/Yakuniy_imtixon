from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Product


def categories_home(request):
    query = request.GET.get('search', '')
    if query:
        categories = Category.objects.filter(name__icontains=query)
    else:
        categories = Category.objects.all()

    # Pagination settings
    paginator = Paginator(categories, 6)  # 6 ta kategoriya har bir sahifada
    page = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,  # To'liq ro'yxat qidiruvlar uchun
        'page_obj': page_obj,  # Faqat hozirgi sahifadagi elementlar
        'query': query,  # Qidiruv qiymatini saqlash
    }
    return render(request, 'categories.html', context)


def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all().order_by('-created_at')  # Mahsulotlarni tartiblash

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
        'total_products': paginator.count,  # Umumiy mahsulotlar soni
    }
    return render(request, 'index.html', context)


def product_search(request):
    query = request.GET.get('q', '').strip()  # Qidiruv so'zini olamiz va bo'sh joylarni olib tashlaymiz
    products = None

    if query:  # Faqat query mavjud bo'lsa, qidiruvni amalga oshiramiz
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        return render(request, 'search_results.html', {
            'query': query,
            'products': None,
            'error': "Please enter a search term."
        })

    paginator = Paginator(products, 6)  # Har bir sahifada 6 ta mahsulot ko'rsatish
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not query:  # Agar qidiruv so'rovi bo'sh bo'lsa
        return render(request, 'index.html', {
            'error': "Please enter a search term to find products.",
        })

    return render(request, 'search_results.html', {
        'query': query,
        'products': page_obj,
    })