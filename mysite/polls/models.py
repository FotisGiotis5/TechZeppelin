from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street} {self.number}, {self.city}"


class Username(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    surname = models.CharField(max_length=255, blank=False)
    address = models.OneToOneField(Address, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"{self.name} {self.surname}"
   

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
     
    def __str__(self):
        return f"Payment of {self.price}"
    
class Manufacturer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class ProductCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=10, blank=False)
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)
    stock = models.IntegerField(
        default=0, blank=False, validators=[MinValueValidator(0)])
    price = models.FloatField(
        default=0.0, blank=False, validators=[MinValueValidator(0)])
    category = models.ForeignKey(ProductCategory, null=True,
                                 on_delete=models.SET_NULL)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    products = models.ManyToManyField(
        Product, related_name='products')
 
    def __str__(self):
        return f"Cart of {self.customer}"
    

class Order(models.Model):
    RECEIVED = 1
    BEING_PROCESSED = 2
    DELIVERED = 3

    ORDER_STATUSES = {RECEIVED, BEING_PROCESSED, DELIVERED}

    id = models.AutoField(primary_key=True)
    status = models.IntegerField()
    date = models.DateTimeField()
    price= models.ForeignKey(Payment, on_delete=models.CASCADE,default=1)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.id} - {self.get_status_display()}"


