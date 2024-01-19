from django.urls import path
""" from .views import customerRegistrationView """
from . import views
from store.views import sellerHomePage


urlpatterns = [
    path('seller-page/', sellerHomePage, name= 'seller-page'),

    path('login-seller/', views.loginSeller, name= 'login-seller'),
    path('register-seller/', views.SellerRegistrationvView, name= 'register-seller'),


    
  
    path('seller-store/', views.sellerStore, name= 'seller-store'),
    path('seller-profile/<str:pk>', views.sellerProfileView, name= 'seller-profile'),

    path('add-product/', views.addProduct, name='add-product'),
    path('delete-product/<str:pk>', views.deleteProduct, name='delete-product'),
    path('update-product/<str:pk>', views.updateProduct, name='update-product'),

]
