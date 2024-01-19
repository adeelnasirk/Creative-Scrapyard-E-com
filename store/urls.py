from django.urls import path
""" from .views import customerRegistrationView """
from . import views 


urlpatterns = [
    path('', views.home, name= 'home'),


    path('login/', views.loginUser, name= 'login'),
    path('logout/', views.logoutUser, name= 'logout'),

    path('register/', views.customerRegistrationView, name= 'register'),


    path('cart/', views.cart, name= 'cart'),
    path('store/', views.store, name= 'store'),
    path('checkout/', views.checkout, name= 'checkout'),

    path('product-detail/<str:pk>/', views.productDetail, name='product-detail'),
    
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order')
]
