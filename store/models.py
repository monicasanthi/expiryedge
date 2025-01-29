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
    product_id= models.CharField(max_length=255)
    quantity= models.CharField(max_length=255)
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