from django.contrib import admin
from .models import Category, Product, Order, Cart, Livraison

# Register your models here.
admin.site.site_header = "GUY-BOUTIQUE"
admin.site.site_title = "GUY-BOUTIQUE"
admin.site.index_title = "Manager"



class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'date_added')

class AdminProduct(admin.ModelAdmin):
    list_display = ('title', 'price', 'category','date_added')
    search_fields = ('title',)
    list_editable = ('price',)

class AdminOrders(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity','prix_total', 'active')
    search_fields = ('user',)
    list_editable = ('product',)

class AdminLivraison(admin.ModelAdmin):
    list_display = ('cart', 'user', 'adresse','ville', 'pays','zipcode','date_commande')
    search_fields = ('user',)
    list_editable = ('user',)

class AdminCart(admin.ModelAdmin):
    list_display = ('user', 'total_prix','prix_livraison', 'total','active','cart_add')
    search_fields = ('user',)
   

admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)
admin.site.register(Order, AdminOrders)
admin.site.register(Cart, AdminCart)
admin.site.register(Livraison, AdminLivraison)


