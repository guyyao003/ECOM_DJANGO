from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']
    def __str__(self) :
         return self.name


class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    image = models.CharField(max_length=5000)
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self) :
         return self.title
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_order")
    quantity = models.IntegerField(default=1)
    prix_total = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def _str_(self) :
        return f"{self.user.username}({self.quantity})"

class Cart(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    total_prix = models.IntegerField(default=0)
    prix_livraison = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    cart_add = models.DateTimeField(auto_now_add=True)
   
    def _str_(self) :
        return f"{self.user.username}({self.active})" 

class Livraison(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    adresse = models.CharField(max_length=200)
    ville = models.CharField(max_length=200)
    pays = models.CharField(max_length=300)
    zipcode = models.CharField(max_length=300)
    date_commande = models.DateTimeField(auto_now=True)

    def _str_(self) :
        return f"{self.user.username})"