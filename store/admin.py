from django.contrib import admin

# Register your models here.
from .models import  *

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(SellerProfile)
admin.site.register(CustomerProfile)


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Order_item)
admin.site.register(Shipping_address)
