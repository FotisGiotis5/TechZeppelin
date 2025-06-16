import json
from .models import Address,Product, ProductCategory,Manufacturer,Order,Cart,OrderItem
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.forms.models import model_to_dict
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from polls import models
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required



PRODUCTS={
    1:{'id':1,'name':'Headset','ProductsCategory':'Gaming Περιφερειακά','Manufacturer':'Razer','price':140.0,'stock':10,'image':'Headset.jpg'},
    2:{'id':2,'name':'Mouse','ProductsCategory':'Περιφερειακά','Manufacturer':'Razer','price':85.0,'stock':10,'image':'Mouse.jpg'},
    3:{'id':3,'name':'Keybord','ProductsCategory':'Gaming Περιφερειακά','Manufacturer':'Razer','price':100.0,'stock':10,'image':'Keybord.jpg'},
    4:{'id':4,'name':'Πληκτρολόγιο','ProductsCategory':'Περιφερειακά','Manufacturer':'PowerTech','price':10.0,'stock':20,'image':'Keybord1.jpg'},
    5:{'id':5,'name':'Ποντίκι','ProductsCategory':'Περιφερειακά','Manufacturer':'Lamtech','price':5.0,'stock':20,'image':'Mouse1.jpg'},
    6:{'id':6,'name':'Ακουστικά','ProductsCategory':'Περιφερειακά','Manufacturer':'Sony','price':8.0,'stock':20,'image':'Headset1.jpg'},
    7:{'id':7,'name':'Κάρτες Γραφικών','ProductsCategory':'PC Hardware','Manufacturer':'Gigabyte','price':240.0,'stock':10,'image':'GPU.jpg'},
    8:{'id':8,'name':'Επεξεργαστές','ProductsCategory':'PC Hardware','Manufacturer':'Ryzen','price':150.0,'stock':10,'image':'CPU.jpg'},
    9:{'id':9,'name':'Μητρικές Κάρτες','ProductsCategory':'PC Hardware','Manufacturer':'Gigabyte','price':88.0,'stock':10,'image':'Motherboard.jpg'},
    10:{'id':10,'name':'Κουτιά Υπολογιστών','ProductsCategory':'Gaming Περιφερειακά','Manufacturer':'PowerTech','price':48.0,'stock':5,'image':'PC.jpg'},
    11:{'id':11,'name':'Μνήμες RAM','ProductsCategory':'PC Hardware','Manufacturer':'Crucial','price':30.0,'stock':20,'image':'Ram.jpg'},
    12:{'id':12,'name':'Ψύκτρες','ProductsCategory':'PC Modding','Manufacturer':'Deepcool','price':49.0,'stock':10,'image':'Air.jpg'},
    13:{'id':13,'name':'Σκληροί Δίσκοι SSD','ProductsCategory':'Δίσκοι','Manufacturer':'Gigabyte','price':20.0,'stock':15,'image':'SSD.jpg'},
    14:{'id':14,'name':'Τροφοδοτικά Υπολογιστή','ProductsCategory':'Τροφοδοτικά Υπολογιστή','Manufacturer':'Deepcool','price':55.0,'stock':10,'image':'PSU.jpg'},
    15:{'id':15,'name':'Εσωτερικοί Σκληροί Δίσκοι','ProductsCategory':'Δίσκοι','Manufacturer':'PowerTech','price':27.0,'stock':6,'image':'HDD.jpg'},
    16:{'id':16,'name':'Ανεμιστηράκια','ProductsCategory':'PC Modding','Manufacturer':'Deepcool','price':5.0,'stock':20,'image':'Fan.jpg'}
}
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
        print("Form data:", request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print("User saved and logged in:", user)
            return redirect('home')
        else:
            print("Form errors:", form.errors)
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})

@login_required
def product_list(request):
    products = Product.objects.all()  # Ανακτούμε όλα τα προϊόντα από τη βάση
    context = {
        'products': products
    }
    return render(request, 'products.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/products')
        else:
            return render(request, 'login.html', {'error': 'Λανθασμένα στοιχεία σύνδεσης'})
    return render(request, 'login.html')

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

def checkout(request):
    cart = request.session.get('cart', [])
    
    if not cart:
        return redirect('cart')  # Αν το καλάθι είναι άδειο, επιστρέφει στο καλάθι
    
    # Υπολογισμός του συνολικού ποσού
    total_price = sum(item['price'] * item['quantity'] for item in cart)
    
    return render(request, 'checkout.html', {
        'cart': cart,
        'total_price': total_price,
    })

def add_to_cart(request):
    if request.method == 'POST':
        selected_products = request.POST.getlist('products')  # Τα ID των προϊόντων από τα checkbox
        cart = request.session.get('cart', [])
        for product_id in selected_products:
            product = PRODUCTS.get(int(product_id))
            if product:
               cart.append({'id':product['id'],
                            'name': product['name'],
                            'category': product['ProductsCategory'],   
                            'manufacturer': product['Manufacturer'],
                            'price':product['price'],
                            'quantity':1})
        request.session['cart']=cart
        return redirect('cart')
    else:
        return HttpResponse('Λάθος μέθοδος')
   
def cart_view(request):
    cart = request.session.get('cart', [])
    total_price=0
    print(cart)
    if isinstance(cart,list):
        try:
           for product in cart:
                if isinstance(product,dict):
                  total_price+=product['price'] 
                else:
                   print("Το product δεν είναι λεξικό")
        except Exception as e:
            print("Λάθος στον υπολογισμό",e)
    else:
        print("Το cart είναι",type(cart),"και όχι λίστα")
   
    return render(request, 'cart.html', {'cart': cart, 'total_price': total_price})

def products_view(request):
    return render(request, 'product_list.html', {'products': PRODUCTS})

def checkout_view(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        # Αν έχεις μοντέλο, αποθηκεύεις:
        # Order.objects.create(full_name=full_name, email=email, phone=phone, address=address)

        messages.success(request, "Η παραγγελία σας καταχωρήθηκε επιτυχώς!")
        return redirect('checkout')  # ή σε μία 'success' σελίδα αν θες


def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    orders_with_items = []

    for order in orders:
        items = OrderItem.objects.filter(order=order)
        orders_with_items.append({'order': order, 'items': items})

    return render(request, 'order_history.html', {'orders_with_items': orders_with_items})

def process_payment(request):
    # Υποθέτουμε ότι η πληρωμή έχει ολοκληρωθεί επιτυχώς
    cart = request.session.get('cart', [])
    
    if not cart:
        return redirect('cart')  # Αν το καλάθι είναι άδειο, επιστρέφει στο καλάθι
    
    # Δημιουργία παραγγελίας
    total_price = sum(item['price'] * item['quantity'] for item in cart)
    order = Order.objects.create(user=request.user, total_price=total_price)
    
    # Δημιουργία των items για την παραγγελία
    for item in cart:
        OrderItem.objects.create(order=order, product_id=item['id'], quantity=item['quantity'], price=item['price'])
    
    # Αδειάζουμε το καλάθι από τη συνεδρία
    request.session['cart'] = []
    
    # Επιστροφή στη σελίδα προϊόντων ή αλλού
    return redirect('order_history')  # Μπορείς να το κατευθύνεις οπουδήποτε θέλεις

def payment(request):
    return redirect('products')

def clear_cart(request):
    request.session['cart'] = []
    return redirect('cart')
    
