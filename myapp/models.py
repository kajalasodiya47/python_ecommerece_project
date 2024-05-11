from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    email = models.EmailField()
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    mobile = models.PositiveBigIntegerField()
    password = models.CharField(max_length=10)
    picture = models.ImageField(default="default.png",upload_to="media/upload")
    role = models.CharField(max_length=10, null=True)


    def __str__(self):
        return self.firstname
    
class Product(models.Model):
    category = (
        ("Men","Men"),
        ("Women","Women"),  
        ("Child","Child")
    )    
    size = (
        ("S","S"),
        ("M","M"),
        ("L","L"),
        ("XL","XL")
    )
    brand = (
        ("Levis","Levis"),
        ("Roadstar","Roadstar"),
        ("Nike","Nike")
    )
    pcategory = models.CharField(max_length=20,choices=category,null=True)
    psize = models.CharField(max_length=20,choices=size,null=True)
    pbrand = models.CharField(max_length=20,choices=brand,null=True)
    seller = models.ForeignKey(User,on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    desc = models.TextField()
    ppicture = models.ImageField(default="",upload_to="ppicture/")
    pname = models.CharField(max_length=20)

class wishlsit(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE) 
    date = models.DateTimeField(default= timezone.now)   

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    product_qty = models.IntegerField(default=1)
    price = models.PositiveIntegerField()
    payment_status = models.BooleanField(default=False)
    total_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.firstname+" | "+self.product.pname
    
class OrderItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE) 
    quantity = models.SmallIntegerField(default=1)  
    

    def __str__(self):
        return f"{self.quantity} of {self.product}" 
    
    def get_item_price(self):
        return self.quantity * self.product.price
    
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    orderDate = models.DateTimeField(blank=True, null=True)
    deliveryDate = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=200,null=True, blank=True)
    mobile = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=500,null=True, blank=True)
    city = models.CharField(max_length=200,null=True, blank=True)
    pincode = models.PositiveIntegerField(null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
          return self.user.firstname

class Ajax(models.Model):
     fname = models.CharField(max_length=20)
     email = models.EmailField(max_length=20)
     mobile = models.PositiveBigIntegerField()

     def __str__(self):
        return self.fname