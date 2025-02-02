from django.shortcuts import render, redirect
from django.contrib import messages
from sympy import Product
from .models import *
from django.utils.timezone import now
from datetime import datetime, timedelta

# Create your views here.
def index(request):
    return render(request,'index.html')

def welcome(request):
    return render(request,'welcome.html')

def about(request):
    return render(request,'about.html')

def staff_dashboard(request):
    return render(request,'staff_dashboard.html')

def product_details(request):
    if request.method=="POST":
        staffid = request.session['id']
        name = request.POST["Product_Name"]
        expiry_date = request.POST["Expiry_Date"]
        product_id = request.POST["Product_id"]
        quantity = request.POST["quantity"]
        mrp = request.POST["mrp"]
        price = request.POST["price"]
        notes = request.POST["notes"]

        productdetails(name=name,staffID=staffid,expiry_date=expiry_date,product_id=product_id,quantity=quantity,notes=notes,mrp=mrp,price=price).save()
        messages.success(request, 'Details stored successfully.')
        return redirect('/p_d/')
    return render(request,'product_details.html')

def product_list(request):
    staffid = request.session['id']
    
    data=productdetails.objects.filter(staffID=staffid)
    return render(request,'product_list.html',{'data':data})

def owner_dashboard(request):
    return render(request,'owner_dashboard.html')

def stock_maintenance(request):
    return render(request,'stock_maintenance.html')

def restock_products(request):
    # Fetch products with quantity less than 5
    to_be_restocked = Product.objects.filter(quantity__lt=5).values('product_name', 'product_id', 'mrp', 'quantity')
    
    # Fetch products with quantity greater than 15
    not_to_be_restocked = Product.objects.filter(quantity__gt=15).values('product_name', 'product_id', 'mrp', 'quantity')
    
    context = {
        'to_be_restocked': to_be_restocked,
        'not_to_be_restocked': not_to_be_restocked,
    }
    
    return render(request, 'restock_products.html', context)
def billing(request):
    if request.method=="POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phoneno = request.POST['phone']
        transactionid = request.POST['transactionid']
        

        productdetails(name=name,email=email,phone=phoneno,transactionid=transactionid).save()
        messages.success(request, 'Details stored successfully.')
        return redirect('/billing/')
    return render(request,'billing.html')

def product_summary(request):
    products = productdetails.objects.all()

    today = datetime.now().date()
    one_day_ago = today - timedelta(days=1)

    categorized_products = {
        'expired': [],
        'expiring_soon': [],
        'good': []
    }

    for product in products:
        try:
            expiry_date = datetime.strptime(product.expiry_date, "%Y-%m-%d").date()
        except ValueError:
            expiry_date = None

        if expiry_date:
            if expiry_date < one_day_ago:  # Ignore expired products older than 1 day
                continue
            elif expiry_date < today:  # Expired (1 day ago)
                categorized_products['expired'].append(product)
            elif (expiry_date - today).days <= 7:  # Expiring within 7 days
                categorized_products['expiring_soon'].append(product)
            else:  # Good products
                categorized_products['good'].append(product)
        else:
            product.notes = "Invalid expiry date"  #  Mark invalid expiry dates if any
            categorized_products['good'].append(product)
 

    return render(request, 'product_summary.html', {'categorized_products': categorized_products})

def expired_product(request):
    
    expired_products=productdetails.objects.all()
    today = datetime.now().date()
    one_day_ago = today - timedelta(days=1)

    expired_products = [
        product for product in expired_products
        if datetime.strptime(product.expiry_date, "%Y-%m-%d").date() < one_day_ago
    ]
    return render(request, 'expired_product.html', {'expired_products': expired_products})

def signup(request):
    if request.method=="POST":
        name = request.POST["name"]
        staffid = request.POST["id"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        email = request.POST["email"]
        password = request.POST["password"]
        usertype = 1
        

        registration(name=name,staffID=staffid,phonenumber=phone,address=address,email=email,password=password, usertype=usertype).save()
        messages.success(request, 'Sucessfully Signed Up.')
        return redirect('/user_signup/')
    return render(request,'sign_up.html')

def user_login(request):
    try:
        if request.method == 'POST':
            email = request.POST["email"]
            password = request.POST["password"]
            user = registration.objects.get(email=email)

            try:
                emp = registration.objects.get(email=email, password=password)
                        
                if emp.userstatus==False:
                    if emp.usertype=='1':
                        messages.success(request, 'You Have Logged In')
                        request.session['email'] = emp.email
                        request.session['id'] = emp.id

                        return redirect('/s_d/')
                    else:
                        messages.success(request, 'Owner Logged In')
                        request.session['email'] = emp.email
                        return redirect('/o_d/')
                else:
                    return redirect('/user_signin/')
            except:
                messages.success(request, 'Invalid Email And Password')
                return redirect('/user_signin/')
    except:
        messages.success(request, 'Something went wrong')
        return redirect('/user_signin/')
    return render(request,'sign_in.html')

def settings(request):
    return render(request, 'settings.html')

def update_profile(request):
    return render(request, 'update_profile.html')

def change_password(request):
    return render(request, 'change_password.html')

def faq(request):
    return render(request, 'faq.html')

def report_issue(request):
    if request.method == "POST":
        staffId = request.session['id']
        name = request.POST["name"]  # Retrieve name from session
        email = request.POST["email"]
        category = request.POST["category"]
        description = request.POST["description"]
        attachment = request.FILES.get("attachment")  # Use request.FILES to get the file

        # Save the data to the model
        issue.objects.create(
            staffID = staffId,
            name=name,
            email=email,
            category=category,
            description=description,
            attachment=attachment
        )

        messages.success(request, 'Details stored successfully.')
        return redirect('/settings/')  # Redirect to the desired page
    return render(request, 'report_issue.html')

def terms_of_service(request):
    return render(request, 'terms_of_service.html')