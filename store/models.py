from django.db import models

# Create your models here.
class registration(models.Model):
    name= models.CharField(max_length=255)
    staffID= models.CharField(max_length=255)
    phonenumber= models.BigIntegerField()
    address= models.CharField(max_length=255)
    email= models.CharField(max_length=255)
    password= models.CharField(max_length=255)
    usertype = models.CharField(max_length=255)
    userstatus= models.BooleanField(default=False) 

class productdetails(models.Model):
    staffID= models.CharField(max_length=255)
    name= models.CharField(max_length=255)
    expiry_date= models.CharField(max_length=255)
    product_id= models.CharField(max_length=6)
    quantity= models.CharField(max_length=255)
    weight = models.CharField(max_length=255)
    mrp= models.CharField(max_length=255, null=True)
    price= models.CharField(max_length=255,null=True)
    notes= models.CharField(max_length=255)
    
class issue(models.Model):
    staffID= models.CharField(max_length=255)
    name= models.CharField(max_length=255)
    email= models.CharField(max_length=255)
    category= models.CharField(max_length=255)
    description= models.CharField(max_length=255)
    attachment= models.ImageField(upload_to='report_issue')

class billing_page(models.Model):
    name= models.CharField(max_length=255)
    email= models.CharField(max_length=255)
    phoneno= models.CharField(max_length=255)
    transactionid= models.CharField(max_length=255)
    address= models.CharField(max_length=255)
    # email = models.EmailField()

class billing_product(models.Model):
    item= models.CharField(max_length=255)
    title= models.CharField(max_length=255)
    weight= models.CharField(max_length=255)
    quantity= models.CharField(max_length=255)
    original_price= models.CharField(max_length=255)
    price= models.CharField(max_length=255)
    total_item= models.CharField(max_length=255)
    sub_total= models.CharField(max_length=255)
    total_tax= models.CharField(max_length=255)
    total= models.CharField(max_length=255)
    payment_method= models.CharField(max_length=255)
    billing_id= models.CharField(max_length=255)