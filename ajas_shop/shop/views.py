from django.shortcuts import render,redirect
from . models import*
from django.contrib import messages
from shop.form import CustomUserFrom
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json

def index(request):
    products=Product.objects.filter(status=0)
    return render(request,"shop/index.html",{"products":products})

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"logged out succesfully")
    return redirect("/")

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            passw=request.POST.get('password')
            user=authenticate(request,username=name,password=passw)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in successfully")
                return redirect("/")
            else:
                messages.error(request,"Invalid Username or Password")
    return render(request,"shop/login.html")

def favviewpage(request):
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        return render(request,"shop/fav.html",{"fav":fav})
    else:
        return redirect("/")

def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            #print(request.user.id)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'already in cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product added'},status=200)
                    else:
                        return JsonResponse({'status':'Product stock not available'},status=200)
            
        else:
            return JsonResponse({'status':'Login to add cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    
def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"shop/cart.html",{"cart":cart})
    else:
        return redirect("/")
    
def fav_page(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=data['pid']
            #print(request.user.id)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'already in favourite'},status=200)
                else:
                    Favourite.objects.create(user=request.user,product_id=product_id)
                    return JsonResponse({'status':'Product added to favourite'},status=200)
            
        else:
            return JsonResponse({'status':'Login to add favourite'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)

def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")

def remove_fav(request,fid):
    cartitem=Favourite.objects.get(id=fid)
    cartitem.delete()
    return redirect("/favviewpage")

def buy_now(request):
    bill=Cart.objects.filter(user=request.user)
    if len(bill)==0:
        return JsonResponse({'status':'Add products to cart'},status=200)
    else:
        return render(request,"shop/buy_now.html",{"bill":bill})

def oder_s(request):
    return render(request,"shop/oder_s.html")
    
def register(request):
    form=CustomUserFrom()
    if request.method=='POST':
        form=CustomUserFrom(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"registered successfully")
            return redirect('/login')
    return render(request,"shop/reg.html",{'form':form})

def collection(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,"shop/collection.html",{"category":catagory})    

def collectionviews(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products=Product.objects.filter(catagory__name=name)
        return render(request,"shop/products/index.html",{"products":products,"category_name":name})
    else:
        messages.warning(request,'NO such Category Name!')
        return redirect("collection")

def product_detials(request,cname,pname):
    if (Catagory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/products/product_detials.html",{"products":products})
        else:
            messages.error(request,'NO such product Name!')
            return redirect("collection")
    else:
        messages.error(request,'NO such Category Name!')
        return redirect("collection")
    