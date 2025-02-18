from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.core.mail import send_mail, EmailMessage
from django.http import JsonResponse
from pyzbar.pyzbar import decode
from django.views.decorators.csrf import csrf_exempt
from django.db.models import IntegerField
from django.db.models.functions import Cast
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import os
from django.conf import settings
import cv2
import numpy as np
import base64
import json

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
        product_id = request.POST["Product_id"][-6:]
        quantity = request.POST["quantity"]
        weight = request.POST["weight"]
        mrp = request.POST["mrp"]
        price = request.POST["price"]
        notes = request.POST["notes"]
 
        print(f"Original Product ID: {request.POST['Product_id']}")
        print(f"Stored Product ID: {product_id}")

        productdetails(name=name,staffID=staffid,expiry_date=expiry_date,product_id=product_id,quantity=quantity,weight=weight,notes=notes,mrp=mrp,price=price).save()
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
    # # Convert 'quantity' to integer for correct filtering
    # products = productdetails.objects.annotate(
    #     quantity_int=Cast('quantity', IntegerField())
    # )

    # Fetch products with quantity less than 5
    to_be_restocked = productdetails.objects.annotate(
        quantity_int=Cast('quantity', IntegerField())
    ).filter(quantity_int__lt=5).values('name', 'product_id', 'mrp', 'quantity')    
    # Fetch products with quantity greater than 15
    not_to_be_restocked = productdetails.objects.annotate(
        quantity_int=Cast('quantity', IntegerField())
    ).filter(quantity_int__gt=15).values('name', 'product_id', 'mrp', 'quantity')    
    context = {
        'to_be_restocked': to_be_restocked,
        'not_to_be_restocked': not_to_be_restocked,
    }

    return render(request, 'restock_products.html', context)

@csrf_exempt
def billing(request):
    if request.method == "POST":
        try:
            product_id = request.POST.get('product_id')
            if not product_id:
                # Try to get from JSON body in case of fetch API
                data = json.loads(request.body)
                product_id = data.get('product_id')

            if product_id:
                # Get last 6 digits if product_id is longer
                product_id = product_id[-6:]
                try:
                    product = productdetails.objects.get(product_id=product_id)
                    return JsonResponse({
                        'success': True,
                        'product': {
                            'name': product.name,
                            'quantity': product.quantity,
                            'mrp': product.mrp,
                            'price': product.price,
                            'expiry_date': product.expiry_date,
                            'weight': product.weight
                        }
                    })
                except productdetails.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': 'Product not found'
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'No product ID provided'
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return render(request, 'billing.html')

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

def user_settings(request):
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

@csrf_exempt
def barcode_scanner(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        image_data = data.get('image')

        if image_data:
            # Convert base64 image to OpenCV format
            encoded_data = image_data.split(',')[1]
            nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Decode barcode
            barcodes = decode(img)
            for barcode in barcodes:
                barcode_data = barcode.data.decode('utf-8')
                return JsonResponse({'barcode': barcode_data})

    return JsonResponse({'barcode': None})

@csrf_exempt
def save_billing(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received data:", data)  # Debug print
            
            # Generate a unique transaction ID
            transaction_id = f"BILL-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Save billing page details
            billing = billing_page.objects.create(
                name=data['customer']['name'],
                email=data['customer']['email'],
                phoneno=data['customer']['phone'],
                address=data['customer']['address'],
                transactionid=transaction_id
            )
            
            # Save each product in the billing
            for item in data['items']:
                print("Processing item:", item)  # Debug print
                billing_product.objects.create(
                    item=str(item['index']),
                    title=item['name'],  
                    weight=item['weight'],
                    quantity=item['quantity'],
                    original_price=item['originalPrice'],  
                    price=item['price'],
                    total_item=len(data['items']),
                    sub_total=data['summary']['subtotal'],
                    total_tax=data['summary']['tax'],
                    total=data['summary']['total'],
                    payment_method='Cash',
                    billing_id=transaction_id
                )

            # Create PDF
            pdf_path = os.path.join(settings.MEDIA_ROOT, f'bill_{transaction_id}.pdf')
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            
            # Generate PDF
            c = canvas.Canvas(pdf_path, pagesize=letter)
            width, height = letter
            
            # Add header
            c.setFont("Helvetica-Bold", 24)
            c.drawString(50, height - 50, "Invoice")
            c.setFont("Helvetica", 12)
            c.drawString(50, height - 80, f"Transaction ID: {transaction_id}")
            c.drawString(50, height - 100, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Add customer details
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, height - 140, "Customer Details")
            c.setFont("Helvetica", 12)
            c.drawString(50, height - 160, f"Name: {data['customer']['name']}")
            c.drawString(50, height - 180, f"Email: {data['customer']['email']}")
            c.drawString(50, height - 200, f"Phone: {data['customer']['phone']}")
            c.drawString(50, height - 220, f"Address: {data['customer']['address']}")
            
            # Create table data
            table_data = [['#', 'Item', 'Weight', 'Quantity', 'Price', 'Total']]
            for item in data['items']:
                table_data.append([
                    str(item['index']),
                    item['name'],
                    item['weight'],
                    item['quantity'],
                    f"₹{item['originalPrice']}",
                    f"₹{item['price']}"
                ])
            
            # Create table
            table = Table(table_data, colWidths=[30, 200, 70, 70, 70, 70])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            # Draw table
            table.wrapOn(c, width, height)
            table.drawOn(c, 50, height - 400)
            
            # Add summary
            c.setFont("Helvetica-Bold", 12)
            c.drawString(400, height - 450, f"Subtotal: ₹{data['summary']['subtotal']}")
            c.drawString(400, height - 470, f"Tax: ₹{data['summary']['tax']}")
            c.drawString(400, height - 490, f"Total: ₹{data['summary']['total']}")
            
            c.save()
            
            # Prepare email content
            email_content = f"""
            Dear {data['customer']['name']},

            Thank you for your purchase! Here are your billing details:

            Transaction ID: {transaction_id}
            Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

            Items Purchased:
            {'='*50}
            """
            
            for item in data['items']:
                email_content += f"""
                {item['name']}
                Quantity: {item['quantity']}
                Price: ₹{item['price']}
                {'='*50}
                """
            
            email_content += f"""
            Summary:
            Subtotal: ₹{data['summary']['subtotal']}
            Tax: ₹{data['summary']['tax']}
            Total: ₹{data['summary']['total']}

            Please find your invoice attached to this email.

            Thank you for shopping with us!
            """
            
            # Send email with PDF attachment
            email = EmailMessage(
                subject=f'Your Invoice - {transaction_id}',
                body=email_content,
                from_email='monicasanthi04@gmail.com',
                to=[data['customer']['email']]
            )
            
            # Attach PDF
            with open(pdf_path, 'rb') as f:
                email.attach(f'invoice_{transaction_id}.pdf', f.read(), 'application/pdf')
            
            email.send(fail_silently=False)
            
            # Clean up PDF file
            os.remove(pdf_path)
            
            return JsonResponse({
                'success': True,
                'message': 'Billing details saved successfully',
                'transaction_id': transaction_id
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })