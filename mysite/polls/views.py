
import json

from .models import Address,Product, ProductCategory
from django.http.response import HttpResponse
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.contrib.auth import login
from polls import models
from .models import Product
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.conf import settings


def address_list(request):
    addresses = Address.objects.all()
    return render(request, "addresses.html", {"addresses": addresses})

def get_products(request):
    selected_category = request.GET.get('category')
    categories = models.ProductCategory.objects.all()

    if selected_category:
        products = models.Product.objects.filter(category__name=selected_category)
    else:
        products = models.Product.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category
    }
    return render(request, 'products.html', context)


def home(request):
    return render(request, 'home.html')  


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Αυτοματοποιημένη σύνδεση μετά την εγγραφή
            return redirect('home')  # Αντικατάστησε με την URL της αρχικής σου σελίδας
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})  

def product_list(request):
    category = request.GET.get("category")
    if category:
        products = Product.objects.filter(category__name=category)
    else:
        products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ο λογαριασμός δημιουργήθηκε επιτυχώς!')
            return redirect('login')  # ή σε άλλη σελίδα
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def home_view(request):
    return render(request, 'home.html', {
        'login_form': AuthenticationForm(),
        'signup_form': SignUpForm()
    })

def contact(request):
    return render(request, 'contact.html')