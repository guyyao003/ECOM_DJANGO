from django.urls import path 
from app003.views import index, detail, checkout, confirmation, connexion, cart, cart_moins, cart_supprimer, deconnexion, inscription

urlpatterns = [
    path('', index, name='home'),
    path('<int:id>', detail, name="detail"),
    path('checkout', checkout, name="checkout"), 
    path('confirmation', confirmation, name="confirmation"), 
    path('connexion', connexion, name="connexion"),
    path('inscription', inscription, name="inscription"),
    path('cart/<int:id>', cart , name="cart"),
    path('cart_moins/<int:id>', cart_moins , name="cart_moins"),
    path('cart_supprimer/<int:id>', cart_supprimer , name="cart_supprimer"),
    path('deconnexion', deconnexion, name="deconnexion"),

]

