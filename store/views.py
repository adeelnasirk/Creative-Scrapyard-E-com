from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q

from django.contrib.auth import authenticate, login, logout
from .models import User,Category, Product, Order, Order_item
from .forms import CustomerRegistrationForm, SellerRegistrationForm, SellerRegistrationForm2
import json
import datetime
# Create your views here.

#Login view 
def loginUser(request):
    page = 'login'
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            return HttpResponse('User does not exits...')
    
        user = authenticate(request, email=email, password=password)
        if user is not None:
            user= login(request, user)
            return redirect('home')
        else:
            return HttpResponse('username or password is incorrect')

    return render(request, 'store/login_register.html', {'page': page})

""" #Seller-Login view 
def loginSeller(request):
    page = 'login'

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            return HttpResponse('User does not exits...')
    
        user = authenticate(request, email=email, password=password)
        if user is not None:
            user= login(request, user)
            return redirect('seller-page')
        else:
            return HttpResponse('username or password is incorrect')

    return render(request, 'store/login_reg_seller.html',  {'page': page})

 """

#Logoutview
def logoutUser(request):
    logout(request)
    return redirect('home')



#register customer

def customerRegistrationView(request):
    form = CustomerRegistrationForm()
    if request.method=="POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            HttpResponse('Please Enter information correctly...')

    context={'form':form}
    return render(request, 'store/login_register.html', context)

""" class customerRegistrationView(CreateView):
    template_name = 'store/login_register.html'
    form_class = CustomerRegistrationForm

    def form_valid(self, form):
        user=form.save()
        login(self.request, user)
        return redirect('home') 
        """
""" 
#Seller registration
def SellerRegistrationvView(request):
    form = SellerRegistrationForm()
    if request.method=='POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            user.save()
            login(request, user)
            return redirect('seller-page')
        else:
            return HttpResponse('Invaid information...')
    return render(request, 'store/login_reg_seller.html', {})
 """

def home(request):

    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.order_item_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_item':0, 'get_cart_total':0}
        cartItems = order['get_cart_item']

    products = Product.objects.all()

    context = {'products': products,'cartItems': cartItems}
    return render(request, 'store/home.html', context)
 

def sellerHomePage(request):
    return render(request, 'seller/seller_page.html', {})


"""
def sellerProfileView(request, pk):
    seller = User.objects.get(id=pk)
    products = seller.product_sel.all()
    context = {'seller':seller, 'products': products}

    return render (request, 'store/seller_profile.html', context)
 """

def store(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    products = Product.objects.filter(
        Q(category__name__icontains=q)|
        Q(name__icontains=q)
    )

    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.order_item_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_item':0, 'get_cart_total':0}
        cartItems = order['get_cart_item']
        
    categorys = Category.objects.all()
    product_count = Product.objects.all().count()

    context = {'products': products,'categorys':categorys, 'product_count': product_count, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def productDetail(request, pk):
    product = Product.objects.get(id=pk)

    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.order_item_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_item':0, 'get_cart_total':0}
        cartItems = order['get_cart_item']
    context = {'product': product, 'cartItems': cartItems}
    return render (request, 'store/productdetail.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.order_item_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_item':0, 'get_cart_total':0}
        cartItems = order['get_cart_item']
    context = {'items':items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.order_item_set.all()
    else:
        items = []
        order = {'get_cart_item':0, 'get_cart_total':0}
    context = {'items':items, 'order': order}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Id:', productId)
    print('action:', action)

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = Order_item.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)
    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()
    return JsonResponse('Item was added', safe=False)


def processOrder(request):

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print(data)

    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer=customer, complete=False)
        total = data['form']['total']
        order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    return JsonResponse('Payment completed', safe=False)


""" if request.user.is_authenticated:
    customer = request.user
    order, create = Order.objects.get_or_create(customer=customer, complete=False)
    total = data['form']['total']
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        Shipping_address.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            country=data['shipping']['country'],
        )
    else:
        print('user not logged in')"""

