from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Product
from .forms import OrderForm

def home(request):
    categories = Category.objects.all()
    return render(request, 'shop/home.html', {'categories': categories})

def search_results(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.none()
    return render(request, 'shop/search_results.html', {'products': products, 'query': query})

def base_context(request):
    categories = Category.objects.all()
    return {'categories': categories}

def product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.info(request, 'Для додавання товару в кошик необхідно авторизуватись.')
        return redirect('login')
    
    product = get_object_or_404(Product, id=product_id)
    
    cart = request.session.get('cart', [])
    cart.append(product.id)
    request.session['cart'] = cart

    return redirect('cart')

def cart_view(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    return render(request, 'shop/cart.html', {'products': products})

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
    request.session['cart'] = cart
    return redirect('cart')

def checkout_view(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    
    price = 0
    for product in products:
        price += product.price

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.products.set(products)
            request.session['cart'] = []
            return redirect('order_success')
    else:
        form = OrderForm()

    return render(request, 'shop/checkout.html', {'form': form, 'products': products, 'price': price})

def order_success_view(request):
    return render(request, 'shop/order_success.html')

def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    query = request.GET.get('search', '')
    sort_by = request.GET.get('sort')
    products = Product.objects.filter(category=category)

    if query:
        products = products.filter(name__icontains=query)

    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    return render(request, 'shop/category.html', {'category': category, 'products': products, 'query': query, 'sort_by': sort_by})

def about_view(request):
    return render(request, 'shop/about.html')

def contact_view(request):
    return render(request, 'shop/contact.html')

