from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.urls import reverse
from . models import *
import random
import requests
from . utils import *
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest,JsonResponse
from datetime import datetime
 
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

    
# Create your views here.

# Logic for buyer index
@never_cache
def index(request):
    product = Product.objects.all()
    return render(request,"index.html",{'product':product})

# Logic for seller index
@never_cache
def sindex(request):
    product= Product()
    product = Product.objects.all()
    return render(request,"sindex.html",{'product':product})
    
# Logic for product show
@never_cache
def product(request,cat):
    product = Product()
    if cat == 'all':
      product = Product.objects.all()
    elif cat == 'men':
      product = Product.objects.filter(pcategory='Men') 
    elif cat == 'women':
      product = Product.objects.filter(pcategory='Women')
    elif cat == 'child':
      product = Product.objects.filter(pcategory='Child')             
    return render(request,"product.html",{'product':product})

# Logic for cart
@never_cache
def cart(request):
    return render(request,"shoping-cart.html")

# Logic for blog
@never_cache
def blog(request):
    return render(request,"blog.html")

# Logic for about
@never_cache
def about(request):
    return render(request,"about.html")

# Logic for contact
@never_cache
def contact(request):
    return render(request,"contact.html")

# Logic for seller, buyer registration
@never_cache
def signup(request):
    if request.method == "POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg1 = "Email is already registered"
            return render(request,"signup.html",{'msg1':msg1})
        except:
            if request.POST['password'] == request.POST['cpassword']:
                User.objects.create(
                    email = request.POST['email'],
                    firstname = request.POST['firstname'],
                    lastname = request.POST['lastname'],
                    mobile = request.POST['mobile'],
                    password = request.POST['password'],
                    role = request.POST['role']
                )
                msg = "Signup Successfully"
                return render(request,"login.html",{'msg':msg})
            else:
                msg1 = "Password and confirm password does not match"
                return render(request,"signup.html",{'msg1':msg1})
    else:    
        return render(request,"signup.html")

# Logic for seller, buyer login 
@never_cache    
def login(request):
    if request.method=="POST":
        try:
             user = User.objects.get(email = request.POST['email'])
             if user.role == "buyer":
                 request.session['email'] = user.email
                 request.session['firstname'] = user.firstname
                 wishlist=wishlsit.objects.filter(user=user)
                 request.session['picture'] = user.picture.url
                 request.session['wishlist'] = len(wishlist)
                 return render(request,"index.html")
             else:
                 request.session['email'] = user.email
                 request.session['firstname'] = user.firstname
                 request.session['picture'] = user.picture.url
                 return render(request,"sindex.html")
        except Exception as e:
            msg1 = "Email or password does not matched!!"
            return render(request,"login.html",{'msg1':msg1})
    else:   
        return render(request,"login.html")   

# Logic for seller, buyer logout
@never_cache
def logout(request):
    try: 
        del request.session['email']
        del request.session['firstname'] 
        del request.session['picture']
        del request.session['wishlist']
        del request.session['cart_count'] 
        del request.session['net_price']
        logout(request)
        request.session.set_expiry(0)
        return redirect('login')
    except:
        return redirect('login') 

# Logic for forgot password    
@never_cache
def fpass(request):
    if request.method == "POST":
        try:
            otp = random.randint(1001,9999)
            url = "https://www.fast2sms.com/dev/bulkV2"

            querystring = {"authorization":"EckAoG5mCNKrdl0tywTqSV2RLWpQJOx8PzZf37isM6I9XHF1aBvhtd2FSKkBR0XlbmNfcTgYoO1LyAM8","variables_values":str(otp),"route":"otp","numbers":request.POST['mobile']}

            headers = {
                 'cache-control': "no-cache"    
            }

            response = requests.request("GET", url, headers=headers, params=querystring)
            request.session['mobile'] = request.POST['mobile']
            request.session['otp'] = otp
            return render(request,"otp.html")
        except:
            return render(request,"fpass.html")    
    else:
         return render(request,"fpass.html") 

# Logic for otp      
@never_cache        
def otp(request):
    if request.method == "POST":
        otp=int(request.session['otp'])
        uotp=int(request.POST['uotp'])
        if otp == uotp:
            del request.session['otp']
            return render(request,"newpassword.html") 
        else:
            msg = "Invalid Otp"
            return render(request,"otp.html",{'msg':msg})
    else:    
        return render(request,"otp.html")  

# Logic for update password   
@never_cache    
def newpassword(request):
       if request.method == "POST":
            user = User.objects.get(mobile=request.session['mobile'])
            if request.POST['newpassword'] == request.POST['cnewpassword']:
                   user.password=request.POST['newpassword']
                   user.save()
                   return render(request,"login.html")
            else:
                   msg = "New password and Confirm new password does not match"
                   return render(request,"newpassword.html",{'msg':msg})          
       else:    
          return render(request,"newpassword.html")

# Logic for change password       
@never_cache       
def cpassword(request):  
   try:  
        user = User.objects.get(email=request.session['email'])
        if request.method == "POST":
            if user.password==request.POST['oldpassword']:
                if request.POST['newpassword'] == request.POST['cnewpassword']:
                    user.password=request.POST['newpassword']
                    user.save()
                    return redirect('logout')
                else:
                    msg1 = "New password and confirm new password does not match"
                    if user.role == "buyer":
                        return render(request,"cpassword.html",{'msg1':msg1})
                    else:
                        return render(request,"scpassword.html",{'msg1':msg1})
            else:
                msg1 = "Old password does not match"   
                if user.role == "buyer":
                        return render(request,"cpassword.html",{'msg1':msg1})
                else:
                    return render(request,"scpassword.html",{'msg1':msg1}) 
        else: 
            if user.role == "buyer":
                    return render(request,"cpassword.html")
            else:
                    return render(request,"scpassword.html")   
   except:  
      return redirect("index")      

# Logic for profile
@never_cache       
def profile(request):
    try:
        user = User.objects.get(email=request.session['email'])
        if request.method == "POST":
            user.email = request.POST['email']
            user.firstname = request.POST['firstname']
            user.lastname = request.POST['lastname']
            user.mobile = request.POST['mobile']
            user.save()
            if "image" in request.FILES:
                user.picture = request.FILES['image']
                user.save()
                request.session['picture'] = user.picture.url
                if user.role == "buyer":
                    return render(request,"profile.html",{'user':user})   
                else:
                    return render(request,"sprofile.html",{'user':user})  
            else:  
                if user.role == "buyer":
                    return render(request,"profile.html",{'user':user})   
                else:
                    return render(request,"sprofile.html",{'user':user})     
        else:
            if user.role == "buyer":
                    return render(request,"profile.html",{'user':user})   
            else:
                    return render(request,"sprofile.html",{'user':user})
    except:
        return redirect('index')       

# Logic for forgot password email        
@never_cache    
def fpass_email(request):
    if request.method == "POST":
      email = request.POST['email']
      code = random.randint(100001,999999)
      request.session['code'] = code
      request.session['email'] = email
      mymailfunction("Welcome to COZA STORE","mymailtemplate",email,{'email':email,'code':code})
      return render(request,"email_verification_code.html")
    else:
      return render(request,"fpass_email.html") 

# Logic for email through verify otp
@never_cache    
def verify_otp(request):    
    if request.method == "POST":
        code=int(request.session['code'])
        ucode=int(request.POST['ucode'])
        if code == ucode:
             del request.session['code']
             return render(request,"new_password.html")
        else:
            return render(request,"email_verification_code.html")
    else:
          return render(request,"email_verification_code.html") 

# Logic for email through update password
@never_cache       
def new_password(request):
    if request.method == "POST":
            user = User.objects.get(email=request.session['email'])
            if request.POST['newpassword'] == request.POST['cnewpassword']:
                   user.password=request.POST['newpassword']
                   user.save()
                   return render(request,"login.html")
            else:
                   msg = "New password and Confirm new password does not match"
                   return render(request,"new_password.html",{'msg':msg})          
    else:    
          return render(request,"new_password.html")

# Logic for add products
@never_cache    
def add_product(request):
    try:
        seller = User.objects.get(email=request.session['email'])
        if request.method == "POST":
            Product.objects.create(
                seller = seller,
                pcategory = request.POST['pcategory'],
                psize = request.POST['psize'],
                pbrand = request.POST['pbrand'],
                pname = request.POST['pname'],
                desc = request.POST['desc'],
                price = request.POST['price'],
                ppicture = request.FILES['ppicture']
            )
            msg = "Product Added Successfully!!"
            return render(request,"addproduct.html",{'msg':msg})
        else: 
            return render(request,"addproduct.html") 
    except:
        return redirect('login')    

# Logic for product views
@never_cache
def view_product(request,cat): 
   try:
        seller = User.objects.get(email=request.session['email'])
        product = Product.objects.filter(seller=seller)   
        if cat == 'all':
           product = Product.objects.all()
        elif cat == 'men':
           product = Product.objects.filter(pcategory='Men') 
        elif cat == 'women':
           product = Product.objects.filter(pcategory='Women')
        elif cat == 'child':
          product = Product.objects.filter(pcategory='Child') 
        return render(request,"view_product.html",{'product':product}) 
   except:
        return redirect('login')    
   
# Logic for show particular product detail
@never_cache
def product_detail(request,pk):
    product = Product.objects.get(pk=pk)
    return render(request,"product-detail.html",{'product':product}) 

# Logic for product edit
@never_cache
def pedit(request,pk):
    product = Product.objects.get(pk=pk)
    if request.method == "POST":
         product.pcategory = request.POST['pcategory']
         product.price = request.POST['price']
         product.pbrand = request.POST['pbrand']
         product.pname = request.POST['pname']
         product.price = request.POST['price']
         product.desc = request.POST['desc']
         try:
              product.ppicture = request.FILES['ppicture']
         except:
              pass
         product.save()
         msg = "Product Updated Successfully !!" 
         return render(request,'pedit.html',{'product':product,'msg':msg})    
    else:
        return render(request,"pedit.html",{'product':product})

# Logic for product delete    
@never_cache    
def pdelete(request,pk):
     product = Product.objects.get(pk=pk)
     product.delete() 
     return redirect("sindex")   

# Logic for buyer product details 
@never_cache
def bpdetails(request,pk):
    try: 
        w = False
        c = False
        user = User.objects.get(email=request.session['email'])
        product = Product.objects.get(pk=pk)
        try:
            wishlsit.objects.get(user=user,product=product)
            w = True
        except:
            pass    
        try:
            Cart.objects.get(user=user,product=product,payment_status=False)
            c = True
        except:
            pass    
        return render(request,"bpdetails.html",{'product':product,'w':w,'c':c})
    except:
        product = Product.objects.get(pk=pk)
        return render(request,"bpdetails.html",{'product':product})

# Logic for product add in wishlist
@never_cache
def addwishlist(request,pk):
    user = User.objects.get(email=request.session['email'])
    product = Product.objects.get(pk=pk)
    wishlsit.objects.create(user=user,product=product)
    return redirect("wishlist")

# Logic for show wishlist product
@never_cache
def wishlist(request):
    try:
        user = User.objects.get(email=request.session['email'])
        wishlist=wishlsit.objects.filter(user=user)
        request.session['wishlist'] = len(wishlist)
        return render(request,"wishlist.html",{'wishlist':wishlist})
    except:
        return render(request,"index.html")

# Logic for delete wishlist product
@never_cache
def delwishlist(request,pk):
    user = User.objects.get(email=request.session['email'])
    product = Product.objects.get(pk=pk)
    wishlist = wishlsit.objects.get(user=user,product=product)
    wishlist.delete()
    return redirect("wishlist")

# Logic for product add in cart
@never_cache
def addcart(request,pk):
    product = Product.objects.get(pk=pk)
    user = User.objects.get(email=request.session['email'])
    Cart.objects.create(user=user,
                        product=product,
                        product_qty=1,
                        price = product.price,
                        total_price = product.price
                        )
    order_qs = Order.objects.filter(user=user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(user=user,product=product).exists():
            order_item = order.items.get(user=user,product=product)
            order_item.quantity += 1
            order_item.save()
        else:
            order_item = OrderItem.objects.create(user=user,product=product)
            Order.objects.get(user=user,ordered=False).items.add(order_item) 
    else:
        order = Order.objects.create(user=user,ordered=False,name = user.firstname,mobile = user.mobile,email = user.email)
        order_item = OrderItem.objects.create(user=user,product=product)
        Order.objects.get(user=user,ordered=False).items.add(order_item) 
    try:
        wishlist_item = wishlsit.objects.get(user=user,product=product)
        if wishlist_item:
            wishlist_item.delete()
    finally:            
        return redirect("cart")

# Logic for show cart product
@never_cache
def cart(request):
    try:
        net_price=0
        user = User.objects.get(email=request.session['email'])
        carts = Cart.objects.filter(user=user,payment_status=False)
        #print(carts)
        order_qs = Order.objects.filter(user=user, ordered=False)
        if order_qs.exists():
            order_object = order_qs.first()
            #print(order_object.name)
        else:
            order_object = Order.objects.create(user=user,ordered=False,name = user.firstname,mobile = user.mobile,email = user.email) 
            order_item = OrderItem.objects.create(user=user,product=product)
            Order.objects.get(user=user,ordered=False).items.add(order_item)
        
        request.session['cart_count'] = len(carts)
        for i in carts:
            net_price += i.total_price 
        request.session['net_price'] = net_price    
        order = Order.objects.get(user=user,ordered=False)  
          
        return render(request,"shoping-cart.html",{'carts':carts,'net_price':net_price,'order_object': order_object,'user':user,'order':order})
    except:
       return render(request,"index.html")

# Logic for delete cart product
@never_cache
def delcart(request,pk):
    user = User.objects.get(email=request.session['email'])
    product = Product.objects.get(pk=pk)
    cart = Cart.objects.get(user=user,product=product,payment_status=False)
    cart.delete()
    return redirect("cart")

# Logic for delete product in quantity
def deleteOneQuantity(request):
    # if request.method == 'POST':
        pk = request.POST['item-id']
        #print("id",item_id)
        item = OrderItem.objects.get(pk=pk)
        if item.quantity == 1:
            cart=Cart.objects.get(pk=pk,payment_status=False)
            cart.delete()
            item.delete()   
        else:
            cart=Cart.objects.get(pk=pk,payment_status=False)
            cart.product_qty -= 1
            cart.total_price = cart.price * cart.product_qty
            cart.save()
            item.quantity -= 1
            item.save()
        return redirect("cart")        

# Logic for add product in quantity
@never_cache
def addOneQuantity(request):
    # if request.method == 'POST':
       # print(pk)
        pk = request.POST['item_id']
        item = OrderItem.objects.get(pk=pk)
        item.quantity += 1
        item.save()
        cart = Cart.objects.get(pk=pk,payment_status=False)
        cart.product_qty += 1
        cart.total_price = cart.price * cart.product_qty
        cart.save()
        return redirect("cart")

# Logic for product order details
def orderDetails(request):
    if request.method == 'POST':
       try: 
        user = User.objects.get(email=request.session['email'])
        order = Order.objects.get(user=user,ordered=False)
        order.address = request.POST['address']
        order.city = request.POST['city']
        order.pincode = request.POST['pincode']
        order.save()
        return redirect("cart")
       except:
          print("error")
          return redirect("cart")  

# Logic for cart data show and billing address show
def Checkout(request):
    try:
        qty=0
        user = User.objects.get(email=request.session.get('email'))  
        orderitem = OrderItem.objects.filter(user=user)
        order = Order.objects.get(user=user,ordered=False)
        cart = Cart.objects.filter(user=user,payment_status=False)
        for j in cart:
            qty += j.product_qty 
        print(qty)    
           
        net_price = request.session.get('net_price', 0)  # Default value if net_price is not in session
        
        if net_price > 2000:
            ship = 0
            total_pr = net_price
        else:
            ship = 100 * qty
            total_pr = net_price + ship
        order.price = total_pr
        order.save()
        return render(request, "checkout_page.html", {'orderitem': orderitem, 'order': order, 'cart': cart, 'ship': ship, 'total_pr': total_pr})
    except:
        return render(request, "checkout_page.html")

# Logic for checkout
def razorpaycheck(request):
    qty=0
    user = User.objects.get(email=request.session.get('email')) 
    orderitem = OrderItem.objects.filter(user=user)
    order = Order.objects.get(user=user,ordered=False)
    cart = Cart.objects.filter(user=user,payment_status=False)
    for j in cart:
        qty += j.product_qty 
    # print("Quantity:",qty)    
    net_price = request.session.get('net_price', 0)  # Default value if net_price is not in session
    
    if net_price > 2000:
        ship = 0
        total_pr = net_price
    else:
        ship = 100 * qty
        total_pr = net_price + ship
    return JsonResponse({
        'total_pr':total_pr 
    })  

# logic for razorpayment success
def success(request):
    user = User.objects.get(email=request.session['email'])
    cart = Cart.objects.filter(user=user,payment_status=False)
    for i in cart:
        i.payment_status = True
        i.save()
    o = Order.objects.get(user=user, ordered=False)
    o.ordered= True
    o.orderDate = datetime.now()
    o.save()
    return render(request,"success.html")

# Logic for user my orders
def myOrders(request):
    user = User.objects.get(email=request.session['email'])
    carts = Cart.objects.filter(user=user,payment_status=True)
    return render(request,"myorders.html",{'carts':carts})
