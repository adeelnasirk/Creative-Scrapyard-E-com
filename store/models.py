from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from .managers import CustomUserManager
# Create your models here.

class User(AbstractBaseUser):

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Role(models.TextChoices):
        CUSTOMER= "CUSTOMER", 'customer'
        SELLER= "SELLER", 'seller'

    base_role = Role.CUSTOMER

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    role = models.CharField(max_length=50, choices=Role.choices)

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role=self.base_role
            return super().save(*args, **kwargs)

    

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


#Customer profile
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_id = models.IntegerField( blank=True, null=True)

#Seller profile
class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Company_name = models.CharField(max_length=200, null=True,blank=True)
    Warehose_location = models.CharField(max_length=200 , null=True, blank=True)
    contact_number = models.IntegerField(null=True, blank=True)


# Customer manager
class CustomerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(role=User.Role.CUSTOMER)
        return queryset

# Sller manager
class SellerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(role=User.Role.SELLER)
        return queryset


#customer proxy model
class Customer(User):
    base_role = User.Role.CUSTOMER
    objects = CustomerManager()

    class Meta:
        proxy = True

    def welcome(self):
        return 'only for customer'

@receiver(post_save, sender=Customer)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role=="CUSTOMER":
        CustomerProfile.objects.create(user=instance)



#seller proxy model
class Seller(User):
    base_role = User.Role.SELLER
    objects = SellerManager()

    class Meta:
        proxy = True

    def welcome(self):
        return 'only for Seller'

@receiver(post_save, sender=Seller)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role=="SELLER":
        SellerProfile.objects.create(user=instance)




""" 

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email= models.EmailField(max_length=200, null=True)

    def __str__(self):
        return self.name

"""

class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name




class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url



class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)

    @property
    def get_cart_total(self):
        orderitems = self.order_item_set.all()
        total = sum([item.get_item_total for item in orderitems])
        return total

    @property
    def get_cart_item(self):
        orderitems = self.order_item_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return str(self.id)
    
class Order_item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_item_total(self):
        total = self.product.price*self.quantity
        return total


class Shipping_address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address