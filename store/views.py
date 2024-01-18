from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from . utils import cookieCart, cartData, guestOrder
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import EmailMessage


def store(request,cat = '-1'):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items  = data['items']

	products = Product.objects.all()
	filteredProducts = []
	if(cat == '-1'):
		filteredProducts = products
	for product in products:
		if product.category == cat:
			filteredProducts.append(product)
   
	context = {'products':filteredProducts, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def cart(request):
    
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items  = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	
	if request.user.is_authenticated and items.exists():
		return render(request, 'store/cart.html', context)
	else:
		return render(request, "authentication/signin.html")
		

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def checkout(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items  = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return 	render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		

	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()
 
	if order.shipping == True:
		ShippingAddress.objects.create(customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			zipcode=data['shipping']['zipcode'],)
  
  
	return JsonResponse('Payment submitted..', safe=False)



def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try another username.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('signup')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 characters!")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = True
        myuser.save()

    

        return redirect('signin')

    return render(request, "authentication/signup.html")


def signin(request):
	if request.method == 'POST':
		username = request.POST['username']
		pass1 = request.POST['pass1']
		user = authenticate(username=username, password=pass1)
        
		if user is not None:
			login(request, user)
			return redirect('store')
		else:
		
			messages.error(request, "Bad Credentials!!")
        
	return render(request, "authentication/signin.html")


def signout(request):
	logout(request)
	return  render(request, "authentication/signin.html")