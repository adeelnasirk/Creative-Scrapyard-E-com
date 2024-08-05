from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.contrib.auth import authenticate, login, logout
from store.models import User, Product, Category, Order, Order_item
from store.forms import CustomerRegistrationForm, SellerRegistrationForm, SellerRegistrationForm2, ProductForm
import json
import datetime
# Create your views here.



#Seller-Login view 
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

    return render(request, 'seller/login_reg_seller.html',  {'page': page})



#Seller registration
def SellerRegistrationvView(request):
    form = SellerRegistrationForm()
    if request.method=='POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            """ user = user.append.role(user.Role.SELLER) """
            user.save()
            login(request, user)
            return redirect('seller-page')
        else:
            return HttpResponse('Invaid information...')
    return render(request, 'seller/login_reg_seller.html', {})



# seller home page
""" def sellerHomePage(request):
    return render(request, 'seller/seller_page.html', {})
 """

def sellerProfileView(request, pk):
    user = User.objects.get(id=pk)

    product = user.product_set.all()
    context = {'user':user, 'product': product}
    return render (request, 'seller/seller_profile.html', context)

# seller store
def sellerStore(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    products = Product.objects.filter(
        Q(category__name__icontains=q)|
        Q(name__icontains=q)
    )
    categorys =Category.objects.all()

    return render(request, 'seller/seller-store.html', {'products':products, 'categorys': categorys})

#add product
@login_required(login_url = 'login-seller')
def addProduct(request):
    products = Product.objects.all()
    categorys = Category.objects.all()
    if request.method=='POST':
        data = request.POST
        image = request.FILES.get('image')
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] !='':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None

        product = Product.objects.create(
            seller=request.user,
            name=data['name'],
            price=data['price'],
            category=category,
            image=image,
        )
        return redirect('seller-page')
    context= {'products':products, 'categorys': categorys}
    return render(request, 'seller/add_product.html', context)


# delete item
@login_required(login_url = 'login-seller')
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.user != product.seller:
        return HttpResponse('You are not allowed here')

    if request.method=='POST':
        product.delete()
        return redirect('seller-page')

    return render(request, 'seller/delete_update.html', {'obj': product})

# update product
@login_required(login_url = 'login-seller')
def updateProduct(request, pk):
    page = 'update'
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.user != product.seller:
        return HttpResponse('You are not allowed here')

    if request.method=='POST':
        form =  ProductForm(request.POST, instance=product) 
        if form.is_valid():
            form.save()
            return redirect('seller-page')
    return render(request, 'seller/delete_update.html', {'page':page , 'form': form})