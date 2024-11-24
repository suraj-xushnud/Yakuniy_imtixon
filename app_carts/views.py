from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

from .models import Cart, CartItem, CartProduct
from app_products.models import Product
from django.contrib import messages


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_products = cart.cart_items.all()

    # Savatdagi umumiy narx
    total_products_price = sum(item.product.current_price * item.quantity for item in cart_products)

    # Yuklash narxi va umumiy summa
    shipping_cost = 10
    total_price = total_products_price + shipping_cost

    # Yetkazib berish sanasi
    expected_delivery = now() + timedelta(days=10)

    context = {
        'cart_products': cart_products,
        'total_products_price': total_products_price,
        'shipping_cost': shipping_cost,
        'total_price': total_price,
        'expected_delivery': expected_delivery,
    }
    return render(request, 'cart.html', context)


@login_required
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    # Mahsulotlar ro‘yxatini olish
    products = Product.objects.all()

    if request.method == 'POST':
        # Mahsulotni olish va savatga qo‘shish
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        # Xabarni ko‘rsatish
        return render(request, 'index.html', {
            'products': products,
            'message': f"{product.name} savatga qo‘shildi!"
        })

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')


@login_required
def increase_quantity(request, product_id):
    """Increase the quantity of a product in the cart."""
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart_product = get_object_or_404(CartProduct, cart=cart, product=product)
    cart_product.quantity += 1
    cart_product.save()
    return redirect('cart')


@login_required
def decrease_quantity(request, product_id):
    """Decrease the quantity of a product in the cart."""
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart_product = get_object_or_404(CartProduct, cart=cart, product=product)
    if cart_product.quantity > 1:
        cart_product.quantity -= 1
        cart_product.save()
    else:
        cart_product.delete()
    return redirect('cart')


@login_required
def checkout_view(request):
    """Display the checkout page."""
    cart = get_object_or_404(Cart, user=request.user)
    cart_products = cart.cartproduct_set.all()
    total_price = sum([item.product.current_price * item.quantity for item in cart_products])
    # Add checkout logic here (e.g., order placement, payment processing)
    messages.success(request, "Checkout process completed successfully!")
    return render(request, 'checkout.html', {'cart_products': cart_products, 'total_price': total_price})


@login_required
def increment_quantity(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


@login_required
def decrement_quantity(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart')


@login_required
def checkout(request):
    # Foydalanuvchining savatini olish
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cart_items.all()
        total_price = sum(item.product.current_price * item.quantity for item in cart_items)

        # Checkout jarayonini qayta ishlash
        # Masalan, buyurtma yaratish yoki savatchani tozalash
        cart.cart_items.all().delete()  # Checkoutdan keyin savatchani tozalash

        return render(request, 'checkout.html', {'total_price': total_price})
    except Cart.DoesNotExist:
        return redirect('cart')  # Agar savatcha mavjud bo'lmasa, savat sahifasiga qaytaring
