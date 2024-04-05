from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .models import Product, Order, Cart, Livraison
from django.core.paginator import Paginator
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        user = request.user
        orders = Order.objects.filter(user=user, active="True")
    else:
        orders = None

    product_object = Product.objects.all()
    item_name = request.GET.get('item-name')
    if item_name != '' and item_name is not None:
        product_object = Product.objects.filter(title__icontains=item_name)
    page = request.GET.get('page', 1)
    paginator = Paginator(product_object, 4)
    try:
        product_object = paginator.page(page)
    except PageNotAnInteger:
        product_object = paginator.page(1)
    except EmptyPage:
        product_object = paginator.page(paginator.num_pages)

    datas = {
        'orders': orders,
        'product_object': product_object,
    }
    return render(request, 'app003/index.html', datas)


def detail(request, id):
    if request.user.is_authenticated:
        user = request.user
        orders = Order.objects.filter(user=user, active="True")
    else:
        orders = None
    product = Product.objects.get(id=id)
    datas = {
        'orders': orders,
        'product': product,
    }
    return render(request, 'app003/detail.html', datas)

def checkout(request):
    cart_number = 0
    if request.user.is_authenticated:
        user = request.user
        orders = Order.objects.filter(user=user, active="True")
        cart = Cart.objects.get(user = user, active= "True")
        for i in orders:
            cart_number += i.quantity
    else:
        orders = None
        cart = None
    if request.method == "POST":
        adresse = request.POST.get('adresse')
        ville = request.POST.get('ville')
        pays = request.POST.get('pays')
        zipcode = request.POST.get('zipcode')
        livraison = Livraison()
        livraison.user = user
        livraison.cart = cart
        livraison.adresse = adresse
        livraison.ville = ville
        livraison.pays = pays
        livraison.zipcode = zipcode
        livraison.save()
        cart.active = "False"
        cart.save()
        for order in orders:
            order.active = "False"
            order.save()
        return redirect('confirmation')
    datas = {
        'orders': orders,
        'cart': cart,
        'cart_number': cart_number,
    }
    return render(request, 'app003/checkout.html', datas)

def confirmation(request):
    return render(request, 'app003/confirmation.html')

def connexion(request):
    if request.user.is_authenticated:
        user = request.user
        orders = Order.objects.filter(user=user, active="True")
    else:
        orders = None
    if request.method == 'POST':
        name = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=name,password=password)
        if user is not None and user.is_active:
            login(request,user)
            
            #### redirection si les infos sont correctes
            return redirect('home')
        else:
            print("login échoué")
           # message = "Merci de vérifiez vos informations"
    datas = {
        'orders': orders,
    }
    return render(request, 'app003/connexion.html', datas)

def cart(request,id):
    user = request.user
    product = Product.objects.get(id=id)
    order, created = Order.objects.get_or_create(user = user, product = product, active = "True")
    if created:
        order.quantity = 1
        order.prix_total = product.price
        order.save()
    else:
        order.quantity += 1
        order.prix_total += product.price
        order.save()
    cart, create = Cart.objects.get_or_create(user = user, active = "True")
    if create:
        cart.orders.add(order)
    else:
        if cart.orders.filter(id=order.id).exists():
            print("L'ordre existe déjà dans le panier.")
        else:
            cart.orders.add(order)
    ptot= Order.objects.filter( user=user ,active = "True").aggregate(
    combined_age=Sum('prix_total')
    )
    cart.total_prix = ptot['combined_age']
    cart.prix_livraison = cart.total_prix*0.1
    cart.total = cart.total_prix + cart.prix_livraison
    cart.save()
    return redirect(request.META.get('HTTP_REFERER', 'checkout'))

def cart_moins(request,id):
    user = request.user
    product = Product.objects.get(id=id)
    order= Order.objects.get(user = user, product = product, active = "True")
    if order.quantity > 1:
        order.quantity -= 1
        order.prix_total -= product.price
        order.save()
        cart = Cart.objects.get(user = user, active = "True")
        ptot= Order.objects.filter( user=user ,active = "True").aggregate(
        combined_age=Sum('prix_total')
        )
        cart.total_prix = ptot['combined_age']
        cart.prix_livraison = cart.total_prix*0.1
        cart.total = cart.total_prix + cart.prix_livraison
        cart.save()
    return redirect(request.META.get('HTTP_REFERER', 'checkout'))

def cart_supprimer(request,id):
    user = request.user
    order= Order.objects.get(user = user, id = id, active = "True")
    cart = Cart.objects.get(user = user, active = "True")
    cart.total_prix -= order.prix_total
    cart.orders.remove(order)
    cart.prix_livraison = cart.total_prix*0.1
    cart.total = cart.total_prix + cart.prix_livraison
    cart.save()
    order.delete()
    return redirect(request.META.get('HTTP_REFERER', 'checkout'))

def deconnexion(request):
    logout(request)
    return redirect('home')

def inscription(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')  # Utilisez request.POST.get() pour obtenir les données du formulaire
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpwd = request.POST.get('confirmpwd')  # corriger 'confirmpwd'

        # Vérifier si le nom d'utilisateur ou l'email existe déjà
        if User.objects.filter(username=username).exists():
            messages.error(request, "Nom d'utilisateur déjà pris, veuillez en essayer un autre.")
            return redirect('inscription')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Cet email a un compte.')
            return redirect('inscription')

        # Validation du nom d'utilisateur
        if len(username) > 15:
            messages.error(request, "Le nom d'utilisateur ne doit pas contenir plus de 15 caractères.")
            return redirect('inscription')
        if len(username) < 4:
            messages.error(request, "Le nom d'utilisateur doit contenir au moins 4 caractères.")
            return redirect('inscription')
        if not username.isalnum():
            messages.error(request, "Le nom d'utilisateur doit être alphanumérique.")
            return redirect('inscription')

        # Validation du mot de passe
        if password != confirmpwd:
            messages.error(request, 'Le mot de passe ne correspond pas!')
            return redirect('inscription')
        try:
            validate_password(password)
        except ValidationError as e:
            # Gérer les erreurs de validation du mot de passe
            messages.error(request, e)
            return redirect('inscription')

        # Création de l'utilisateur
        my_user = User.objects.create_user(username=username, email=email, password=password)
        my_user.first_name = firstname
        my_user.last_name = lastname
        my_user.is_active = True
        my_user.save()

        # Authentification et redirection si les informations sont correctes
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('connexion')

    return render(request, 'app003/inscription.html')

