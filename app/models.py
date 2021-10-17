from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
STATE_CHOICE = (
  ('Dhaka',"Dhaka"),
  ('Farmget','Farmget'),
  ('West Razabazar','West Razabazar'),
  ('Tollabag','Tollabag'),
  ('Dhanmondi','Dhanmondi'),
)
# Create your models here.
class Customer(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name= models.CharField(max_length=200)
  locality= models.CharField(max_length=200)
  city= models.CharField(max_length=200)
  zipcode= models.IntegerField()
  state= models.CharField(max_length=50,choices=STATE_CHOICE)
  

  def __str__(self):
    return str(self.id)

CATEGORY_CHOICES = (
  ('M','Mobile'),
  ('L','Laptop'),
  ('TW','Top Wear'),
  ('BW','Bottom Wear'),
)

class Product(models.Model):
  title = models.CharField(max_length=100)
  selling_price = models.FloatField()
  discount_price = models.FloatField()
  description = models.TextField()
  brand = models.CharField(max_length=100)
  category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
  product_image = models.ImageField(upload_to = 'producting')

  def __str__(self):
    return str(self.id)
  
class Cart(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)


  def __str__(self):
    return str(self.id)
  @property
  def total_cost(self):
    return self.quantity * self.product.discount_price

STATUS_CHOICE = (
  ('Accepted','Accepted'),
  ('Packed','Packed'),
  ('On The Way','On The Way'),
  ('Delivered','Delivered'),
  ('Cancle','Cancle'),
)

class OrderPlace(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)
  ordered_date = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=50,choices=STATUS_CHOICE,default='pending')

  @property
  def total_cost(self):
    return self.quantity * self.product.discount_price