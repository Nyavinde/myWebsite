from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=250,null=True,blank=True)
    joined_on = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.full_name

class Team(models.Model):
    title = models.CharField(max_length=300)
    image = models.ImageField(upload_to="images")
    position = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    Category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products")
    selling_price = models.PositiveIntegerField()


    def __str__(self):
        return self.title


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True,blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Cart: '+ str(self.id)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    rate = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()


    def __str__(self):
        return 'Cart: ' + str(self.cart.id) + 'CartProduct: ' + str(self.id)

ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)

METHOD = (
        ("Cash On Delivery","Cash On Dlivery"),
        ("Khalti", "Khalti"),
        ("PayPal", "PayPal"),
)
class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=250)
    shipping_address= models.CharField(max_length=250)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    total = models.PositiveIntegerField(null=True)
    order_status = models.CharField(max_length=50,choices=ORDER_STATUS,null=True)
    payment_method = models.CharField(max_length=20, choices=METHOD, default="Cash On Delivery")
    payment_completed = models.BooleanField(default=False, null=True, blank=True)


    def __str__(self):
        return 'Order: ' + str(self.id )

    class PaymentSelections(models.Model):

        name = models.CharField(verbose_name=("name"),
                help_text=("Required"),
                max_length=255,)

        class Meta:
            verbose_name = ("Payment Selection")
            verbose_name_plural = ("Payment Selections")

        def __str__(self):
            return self.name
