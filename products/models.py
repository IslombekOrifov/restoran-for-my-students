from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from .services import upload_product_image_path

from accounts.models import CustomUser
from accounts.validators import validate_image


class Category(models.Model):
    title = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, blank=True)
    priority = models.PositiveIntegerField(default=0)
    # def save(self):
    #     if self.title:
    #         self.slug = slugify(self.title)


    def __str__(self):
        return self.title
    

class Product(models.Model):
    title = models.CharField(max_length=50)
    price = models.PositiveBigIntegerField()
    image = models.ImageField(
        upload_to=upload_product_image_path, 
        validators=[validate_image], 
        blank=True, null=True
    )
    real_price = models.PositiveBigIntegerField()
    count_all = models.PositiveIntegerField()
    count_sold = models.PositiveIntegerField()
    description = models.CharField(max_length=70, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    
class Order(models.Model):
    waiter = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    price_all = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    price = models.PositiveBigIntegerField()
    product_count = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title



    
    

    
    
