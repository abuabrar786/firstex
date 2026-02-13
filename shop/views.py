from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, Order, OrderItem, Product


def _cart_from_session(request):
    return request.session.get('cart', {})


def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def _next_or_default(request, default='product_list'):
    return request.POST.get('next') or request.GET.get('next') or default


def register(request):
    if request.user.is_authenticated:
        return redirect('product_list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome to the store!')
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def product_list(request):
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()

    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category_id:
        products = products.filter(category_id=category_id)

    return render(
        request,
        'shop/product_list.html',
        {
            'products': products,
            'categories': categories,
            'query': query,
            'selected_category': category_id,
        },
    )


@login_required
def add_to_cart(request, product_id):
    if request.method != 'POST':
        return redirect('product_list')

    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = _cart_from_session(request)
    key = str(product.id)

    if product.stock <= cart.get(key, 0):
        messages.warning(request, f'Only {product.stock} item(s) available in stock.')
    else:
        cart[key] = cart.get(key, 0) + 1
        _save_cart(request, cart)
        messages.success(request, f'{product.name} added to cart.')

    return redirect(_next_or_default(request))


@login_required
def remove_from_cart(request, product_id):
    if request.method != 'POST':
        return redirect('cart_view')

    cart = _cart_from_session(request)
    key = str(product_id)
    quantity = cart.get(key, 0)

    if quantity > 1:
        cart[key] = quantity - 1
        messages.info(request, 'Item quantity reduced by 1.')
    elif quantity == 1:
        del cart[key]
        messages.info(request, 'Item removed from cart.')

    _save_cart(request, cart)
    return redirect(_next_or_default(request, 'cart_view'))


@login_required
def cart_view(request):
    cart = _cart_from_session(request)
    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=product_ids, is_active=True)

    cart_items = []
    total = Decimal('0.00')
    for product in products:
        quantity = cart.get(str(product.id), 0)
        if quantity <= 0:
            continue
        subtotal = product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        total += subtotal

    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def checkout(request):
    cart = _cart_from_session(request)
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('product_list')

    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=product_ids, is_active=True)

    cart_items = []
    total = Decimal('0.00')
    for product in products:
        quantity = cart.get(str(product.id), 0)
        if quantity <= 0:
            continue
        subtotal = product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        total += subtotal

    if request.method == 'POST':
        order = Order.objects.create(user=request.user, status='PLACED')
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price_at_purchase=item['product'].price,
            )
        _save_cart(request, {})
        messages.success(request, f'Order #{order.id} placed successfully.')
        return redirect('order_summary', order_id=order.id)

    return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'total': total})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'shop/order_history.html', {'orders': orders})


@login_required
def order_summary(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related('items__product'), id=order_id, user=request.user)
    return render(request, 'shop/order_summary.html', {'order': order})
