from django.contrib.auth import login
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from .forms import CustomerRegistrationFrom,CustomerProfileform
from .models import Customer,Product,Cart,OrderPlace
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductView(View):
  def get(self,request):
    totalitem=0
    topwears = Product.objects.filter(category='TW') 
    bottomwears = Product.objects.filter(category='BW') 
    mobiles = Product.objects.filter(category='M') 
    laptop = Product.objects.filter(category='L') 
    if request.user.is_authenticated:
      totalitem =len(Cart.objects.filter(user=request.user))
    return render(request,'app/home.html',
     {'topwears':topwears,'bottomwears': bottomwears,
     'mobiles':mobiles,'laptop':laptop,'totalitem':totalitem})



class ProductDetailView(View):
  def get(self, request,pk):
    product = Product.objects.get(pk=pk)
    
    item_already_in_cart = False
    totalitem =0
    if request.user.is_authenticated:
      totalitem =len(Cart.objects.filter(user=request.user))
      item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    return render(request, 'app/productdetail.html',{'product':product,
    'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})

@login_required
def add_to_cart(request):
  totalitem =0
  if request.user.is_authenticated:
    totalitem =len(Cart.objects.filter(user=request.user))
  user=request.user
  product_id = request.GET.get('prod_id')
  product =Product.objects.get(id=product_id)
  Cart(user=user,product=product).save()
  return redirect('/cart')

@login_required
def show_cart(request):
  totalitem=0
  if request.user.is_authenticated:
    totalitem =len(Cart.objects.filter(user=request.user))
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    totalamount=0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
      for p in cart_product:
        tempamount=(p.quantity * p.product.discount_price)
        amount += tempamount
        totalamount=amount+shipping_amount
      context={'carts':cart,'totalamount':totalamount,'amount':amount,'totalitem':totalitem}
      return render(request, 'app/addtocart.html',context)
    else:
      return render(request,'app/empty.html')

def plus_cart(request):
  if  request.method == "GET":
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()
    amount=0.0
    shipping_amount=70.0
    totalamount=0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount=(p.quantity * p.product.discount_price)
      amount += tempamount
      

    data = {
      'quantity': c.quantity,
      'amount': amount,
      'totalamount' :amount+shipping_amount
    }
        
    return JsonResponse(data)

def minus_cart(request):
  if  request.method == "GET":
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity -= 1
    c.save()
    amount=0.0
    shipping_amount=70.0
    totalamount=0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount=(p.quantity * p.product.discount_price)
      amount += tempamount
      

    data = {
      'quantity': c.quantity,
      'amount': amount,
      'totalamount' :amount+shipping_amount
    }
        
    return JsonResponse(data)

@login_required
def remove_cart(request):
  if  request.method == "GET":
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    
    c.delete()
    amount=0.0
    shipping_amount=70.0
    totalamount=0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount=(p.quantity * p.product.discount_price)
      amount += tempamount
     

    data = {
      
      'amount': amount,
      'totalamount' :amount+shipping_amount
    }
        
    return JsonResponse(data)


def buy_now(request):
  

  return render(request, 'app/buynow.html')

@login_required
def address(request):
  totalitem =0
  if request.user.is_authenticated:
    totalitem =len(Cart.objects.filter(user=request.user))
  add = Customer.objects.filter(user=request.user)
  return render(request, 'app/address.html',
  {'totalitem':totalitem,'add':add,'active':'btn-primary'})
@login_required
def orders(request):
  totalitem =0
  if request.user.is_authenticated:
    totalitem =len(Cart.objects.filter(user=request.user))
  op = OrderPlace.objects.filter(user=request.user)
  return render(request, 'app/orders.html',{'order_place':op,'totalitem':totalitem})

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request, data=None):
  totalitem =0
  if request.user.is_authenticated:
    totalitem =len(Cart.objects.filter(user=request.user))
  if data == None:
    mobiles = Product.objects.filter(category = "M")
  elif data == 'Redmi' or data == 'Samsung':
    mobiles = Product.objects.filter(category = "M").filter(brand=data)
  elif data == 'below':
    mobiles = Product.objects.filter(category = "M").filter(discount_price__lt=10000)
  elif data == 'above':
    mobiles = Product.objects.filter(category = "M").filter(discount_price__gt=10000)
  return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitem':totalitem})

def laptop(request, data=None):
  totalitem =0
  if request.user.is_authenticated:
    totalitem =len(Cart.objects.filter(user=request.user))
  if data == None:
    laptop = Product.objects.filter(category = "L")
  elif data == 'Asus' or data == 'HP':
    laptop = Product.objects.filter(category = "L").filter(brand=data)
  elif data == 'below':
    laptop = Product.objects.filter(category = "L").filter(discount_price__lt=50000)
  elif data == 'above':
    laptop = Product.objects.filter(category = "L").filter(discount_price__gt=50000)
  return render(request, 'app/laptop.html',{'laptop':laptop,'totalitem':totalitem})

def topwear(request, data=None):
  totalitem =0
  if request.user.is_authenticated:
    totalitem =len(Cart.objects.filter(user=request.user))
  if data == None:
    tw = Product.objects.filter(category = "TW")
  elif data == 'KORRA' or data == 'Levies':
    tw = Product.objects.filter(category = "TW").filter(brand=data)
  elif data == 'below':
    tw = Product.objects.filter(category = "TW").filter(discount_price__lt=500)
  elif data == 'above':
    tw = Product.objects.filter(category = "TW").filter(discount_price__gt=500)
  return render(request, 'app/topwear.html',{'tw':tw,'totalitem':totalitem})

def btmwear(request, data=None):
  totalitem =0
  if request.user.is_authenticated:
    totalitem =len(Cart.objects.filter(user=request.user))
  if data == None:
    bw = Product.objects.filter(category = "BW")
  elif data == 'KORRA' or data == 'Levies':
    bw = Product.objects.filter(category = "BW").filter(brand=data)
  elif data == 'below':
    bw = Product.objects.filter(category = "BW").filter(discount_price__lt=500)
  elif data == 'above':
    bw = Product.objects.filter(category = "BW").filter(discount_price__gt=500)
  return render(request, 'app/btmwear.html',{'bw':bw,'totalitem':totalitem})



class CustomerRegistrationView(View):
  def get(self, request):
    form = CustomerRegistrationFrom()
    return render(request, 'app/customerregistration.html',{'form':form})
  def post(self, request):
    form = CustomerRegistrationFrom(request.POST)
    if form.is_valid():
      messages.success(request,"Congratulations!!! Registered successfully")
      form.save()
    return render(request, 'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
  totalitem =0
  if request.user.is_authenticated:
    totalitem =len(Cart.objects.filter(user=request.user))
  user =request.user
  add= Customer.objects.filter(user=user)
  cart_items =Cart.objects.filter(user=user)
  amount= 0.0
  shipping_amount = 70.0
  totalamount=0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  if cart_product:

    for p in cart_product:
      tempamount=(p.quantity * p.product.discount_price)
      amount += tempamount
    totalamount = amount+shipping_amount
   
  context={'add':add,'totalamount':totalamount,'cart_items':cart_items,'totalitem':totalitem}
  return render(request, 'app/checkout.html',context)

@login_required
def payment_done(request):
  user =request.user
  custid=request.GET.get('custid')
  customer = Customer.objects.get(id=custid)
  cart = Cart.objects.filter(user=user)
  for c in cart:
    OrderPlace(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
    c.delete()
  return redirect("orders")

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
  def get(self,request):
    totalitem =0
    if request.user.is_authenticated:
      totalitem =len(Cart.objects.filter(user=request.user))
    form = CustomerProfileform()
    return render(request,'app/profile.html',{'totalitem':totalitem,'form':form,
    'active':'btn-primary'})
  def post(self,request):
    totalitem =0
    if request.user.is_authenticated:
      totalitem =len(Cart.objects.filter(user=request.user))
    form = CustomerProfileform(request.POST)
    if form.is_valid():
      usr = request.user
      name = form.cleaned_data['name']
      locality = form.cleaned_data['locality']
      city = form.cleaned_data['city']
      state = form.cleaned_data['state']
      zipcode = form.cleaned_data['zipcode']
      reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
      reg.save()
      messages.success(request,'Congratulations profile Updated successfully!!!!')
    return render(request,'app/profile.html',{'totalitem':totalitem,'form':form,
    'active':'btn-primary'})