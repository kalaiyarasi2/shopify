from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category
from marketing.models import Subscriber
from django.contrib import messages
from django.http import JsonResponse

def home(request):
    featured_products = Product.objects.filter(available=True)[:8]
    categories = Category.objects.all()
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)

def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'category': category,
    }
    return render(request, 'store/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    variants = product.variants.all()
    related_products = Product.objects.filter(
        category=product.category, available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'variants': variants,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)

def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, 'Thank you for subscribing!')
            else:
                messages.info(request, 'You are already subscribed!')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})