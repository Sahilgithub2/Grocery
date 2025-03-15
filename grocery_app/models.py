from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255,null=False, blank=False)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image_url = models.URLField(default="https://cdn.pixabay.com/photo/2016/08/11/08/43/potatoes-1585060_1280.jpg")
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=101, blank=True, null=True)
    
    def __str__(self):
        return self.name 


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"        
