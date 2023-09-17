from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

class userManager(BaseUserManager):
    def create_user(self,username,password,**extra_fields):
        if not username:
            raise ValueError("Username should be provided")
        user = self.model(username=username,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,username,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(username,password,**extra_fields)

class User(AbstractBaseUser):
    id=models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=100,unique=True)
    email = models.CharField(max_length=60)
    mobile_number = models.CharField(max_length=12)
    password = models.CharField(max_length=16)
 
    USERNAME_FIELD = 'username'
    objects =userManager()


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    image = models.TextField(blank=True, null=True)
    brand = models.CharField(max_length=100)
    shipping = models.TextField()
    description = models.TextField()
    price = models.FloatField(default=0.0)
    category = models.CharField(max_length=100)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
                    models.Index(fields=["name"],name="name-index"),
                    models.Index(fields=["category","brand"],name="category-brand-index")
        ]

class Order(models.Model):
    #user=models.ForeignKey(User,on_delete=models.CASCADE)
    user = models.IntegerField()
    order_number = models.CharField(max_length=20)
    order_date = models.DateTimeField(auto_now_add=True)
    order_item = models.OneToOneField(
        "OrderItem",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="order_detail",
    )


class OrderItem(models.Model):
    order =models.IntegerField()
    product = models.IntegerField()
    quantity = models.PositiveIntegerField()
    price = models.FloatField()



class Review(models.Model):

    user = models.IntegerField()
    product = models.IntegerField()
    rate = models.PositiveIntegerField()
    review = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)


class BillingAddress(models.Model):
    order = models.IntegerField()
    address = models.TextField()
    city = models.CharField(max_length=300)


class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.FloatField()
    orders = models.ManyToManyField(Order, related_name="order")



