from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from grocery_app.forms import LoginForm
from decimal import Decimal
from grocery_app.models import Product, Cart
import json
from django.contrib.auth.models import User
from django.http import HttpResponse
from captcha.helpers import captcha_image_url
from captcha.image import ImageCaptcha
from captcha.models import CaptchaStore
from django.views.decorators.csrf import csrf_exempt
import json
import os
import requests  # Used to call the real payment gateway API
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from grocery_app.forms import LoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.views.decorators.csrf import csrf_exempt


from django.http import JsonResponse
from grocery_app.models import Product

from django.http import JsonResponse
from .models import Product
from django.http import JsonResponse
from grocery_app.models import Product

def filter_products(request):
    category = request.GET.get("category", "").strip()
    subcategory = request.GET.get("subcategory", "").strip()

    print(f"🔎 Filtering: Category='{category}', Subcategory='{subcategory}'")  # Debugging Output

    # Fetch products by category (case insensitive)
    products = Product.objects.filter(category__iexact=category)

    # If a subcategory is selected (not 'All'), apply filter
    if subcategory and subcategory.lower() != "all":
        products = products.filter(subcategory__iexact=subcategory)

    product_list = list(products.values("id", "name", "price", "image_url", "subcategory"))

    print(f"📌 Found {len(product_list)} products")  # Debugging Output

    return JsonResponse({"products": product_list})

# def filter_products(request):
#     category = request.GET.get("category", "")
#     subcategory = request.GET.get("subcategory", "")

#     # Handling Vegetables as before
#     if category == "Vegetable":
#         products = Product.objects.filter(category=category)
#         if subcategory and subcategory != "All":
#             products = products.filter(subcategory=subcategory)
    
#     # Separate logic for Fruits
#     elif category == "Fruit":
#         products = Product.objects.filter(category="Fruit")
        
#         # Apply subcategory filter for Fruits
#         if subcategory and subcategory != "All":
#             products = products.filter(subcategory=subcategory)

#     # Separate logic for Eggs & Poultr  y
#     elif category in ["Eggs", "Poultry", "Chicken", "Duck", "Turkey", "Quail", "Goose"]:
#         # Since poultry types are related, we fetch everything under "Eggs & Poultry"
#         if category == "Eggs":
#             products = Product.objects.filter(category="Eggs")
#         else:
#             products = Product.objects.filter(category="Poultry", subcategory=category)

#     else:
#         products = Product.objects.none()  # If no valid category is found, return an empty list

#     # Convert queryset to JSON response
#     product_list = list(products.values("id", "name", "price", "image_url", "subcategory"))

#     return JsonResponse({"products": product_list})




@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("email-or-phone")
        password = request.POST.get("password")

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"success": True, "message": "Login successful!"})
        else:
            return JsonResponse({"success": False, "error": "Invalid username or password."})

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def sign_up_view(request):
    if request.method == "POST":
        username = request.POST.get("sign-up-email-or-phone")
        password = request.POST.get("sign-up-password")
        confirm_password = request.POST.get("confirm-password")

        # Check if passwords match
        if password != confirm_password:
            return JsonResponse({"success": False, "error": "Passwords do not match."})

        # Check if username exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "error": "Username already taken."})

        # Create user and save in DB
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return JsonResponse({"success": True, "message": "Account created successfully!"})

    return JsonResponse({"error": "Invalid request method"}, status=405)# Create your views here.
def cart_view(request):
    return render(request, "cart.html")

def fruits_view(request):
    return render(request, "fruits.html")

def vegetables_view(request):
    return render(request, "vegetables.html")

def index_view(request):
    return render(request, "index.html")

def eggs_view(request):
    return render(request, "eggs.html")

def add_product(request):
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        price = request.POST.get('price')
        image_url = request.POST.get('image_url')
        category = request.POST.get('category', 'Uncategorized')

        # Validate required fields
        if not name:
            return JsonResponse({'error': 'Product name is required'}, status=400)
        if not price:
            return JsonResponse({'error': 'Product price is required'}, status=400)
        if not image_url:
            return JsonResponse({'error': 'Product image URL is required'}, status=400)

        # Create or get product
        product, created = Product.objects.get_or_create(
            name=name,
            defaults={
                'price': price,
                "image_url": requests.get("image_url", ""),
                'category': category,
            }
        )

        if not created:
            return JsonResponse({'message': 'Product already exists'}, status=400)

        return JsonResponse({'message': 'Product added successfully', 'product_id': product.id})

    return JsonResponse({'error': 'Invalid request method'}, status=400)



def captcha_refresh(request):
    """Generates a new CAPTCHA and returns the image URL and key."""
    new_key = CaptchaStore.generate_key()
    new_image_url = captcha_image_url(new_key)
    
    return JsonResponse({'key': new_key, 'image_url': new_image_url})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from grocery_app.models import Product, Cart

# @csrf_exempt  # Disable CSRF for testing (not recommended in production)
# def add_to_cart(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)  # Read JSON from request
#             product_id = data.get('product_id')

#             if not product_id:
#                 return JsonResponse({"error": "Product ID is required"}, status=400)

#             product = Product.objects.get(id=product_id)  # Fetch product

#             if request.user.is_authenticated:
#                 user = request.user  # ✅ Use the logged-in user
#             else:
#                 return JsonResponse({"error": "User not authenticated"}, status=401)

#             # Add product to cart for the authenticated user
#             cart_item, created = Cart.objects.get_or_create(user=user, product=product)
#             if not created:
#                 cart_item.quantity += 1
#             cart_item.save()

#             return JsonResponse({
#                 "message": "Product added to cart",
#                 "product": product.name,
#                 "quantity": cart_item.quantity
#             })

#         except Product.DoesNotExist:
#             return JsonResponse({"error": "Product not found"}, status=404)
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON"}, status=400)

#     return JsonResponse({"error": "Invalid request method"}, status=405)
@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')

            print(f"🔹 Received Add Request for Product ID: {product_id}")  # Debugging

            if not product_id:
                return JsonResponse({"error": "Product ID is required"}, status=400)

            try:
                product = Product.objects.get(id=int(product_id))
            except Product.DoesNotExist:
                print(f"❌ Product ID {product_id} does not exist in DB")  # Debugging
                return JsonResponse({"error": "Product not found"}, status=404)

            if request.user.is_authenticated:
                user = request.user
            else:
                user, _ = User.objects.get_or_create(username="guest_user")

            cart_item, created = Cart.objects.get_or_create(user=user, product=product)

            if not created:
                cart_item.quantity += 1
            cart_item.save()

            return JsonResponse({
                "message": "Product added to cart",
                "product_id": product.id,  # ✅ Return correct Product ID
                "quantity": cart_item.quantity
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


# @csrf_exempt  # Disable CSRF for testing (NOT recommended for production)
# def remove_from_cart(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)  # Read JSON from request
#             product_id = data.get('product_id')

#             if not product_id:
#                 return JsonResponse({"error": "Product ID is required"}, status=400)

#             try:
#                 product = Product.objects.get(id=product_id)  # Fetch product
#             except Product.DoesNotExist:
#                 return JsonResponse({"error": "Product not found"}, status=404)

#             if not request.user.is_authenticated:
#                 return JsonResponse({"error": "User not authenticated"}, status=401)

#             user = request.user  # ✅ Use the logged-in user

#             try:
#                 cart_item = Cart.objects.get(user=user, product=product)
#                 if cart_item.quantity > 1:
#                     cart_item.quantity -= 1
#                     cart_item.save()
#                     quantity = cart_item.quantity  # ✅ Safe reference after save()
#                 else:
#                     cart_item.delete()
#                     quantity = 0  # ✅ Avoid referencing deleted object

#                 return JsonResponse({
#                     "message": "Product removed from cart",
#                     "product": product.name,
#                     "quantity": quantity  # ✅ Ensure valid quantity reference
#                 })

#             except Cart.DoesNotExist:
#                 return JsonResponse({"error": "Product not in cart"}, status=404)

#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON"}, status=400)

#     return JsonResponse({"error": "Invalid request method"}, status=405)
#@csrf_exempt
@csrf_exempt
def remove_from_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')

            print(f"🔹 Received remove request for Product ID: {product_id}")  # Debugging

            if not product_id:
                return JsonResponse({"error": "Product ID is required"}, status=400)

            try:
                product = Product.objects.get(id=int(product_id))
            except Product.DoesNotExist:
                print(f"❌ Product with ID {product_id} not found in DB")
                return JsonResponse({"error": "Product not found"}, status=404)

            if not request.user.is_authenticated:
                return JsonResponse({"error": "User not authenticated"}, status=401)

            user = request.user
            try:
                cart_item = Cart.objects.get(user=user, product=product)

                print(f"✅ Found in Cart: {cart_item}")  # Debugging

                cart_item.delete()
                return JsonResponse({"success": True, "message": "Product removed from cart"})

            except Cart.DoesNotExist:
                print(f"❌ Product {product_id} not found in User's Cart")
                return JsonResponse({"error": "Product not in cart"}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

# import json
# from django.http import JsonResponse

# @csrf_exempt
# def update_cart(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             print("🔹 Received Data:", data)  # ✅ Debugging Line

#             product_id = data.get("product_id")
#             action = data.get("action")

#             if not product_id or not action:
#                 return JsonResponse({"error": "Missing product ID or action"}, status=400)

#             # Check if product exists
#             try:
#                 product = Product.objects.get(id=product_id)
#             except Product.DoesNotExist:
#                 return JsonResponse({"error": "Product not found"}, status=404)

#             # Check if item is in cart
#             try:
#                 cart_item = Cart.objects.get(user=request.user, product=product)
#             except Cart.DoesNotExist:
#                 return JsonResponse({"error": "Item not in cart"}, status=404)

#             # Increase or decrease quantity
#             if action == "increase":
#                 cart_item.quantity += 1
#                 cart_item.save()
#             elif action == "decrease":
#                 if cart_item.quantity > 1:
#                     cart_item.quantity -= 1
#                     cart_item.save()
#                 else:
#                     cart_item.delete()

#             print(f"✅ Updated {cart_item.product.name} to Quantity: {cart_item.quantity}")
#             return JsonResponse({"message": "Cart updated", "quantity": cart_item.quantity})

#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON"}, status=400)

#     return JsonResponse({"error": "Invalid request method"}, status=405)

def index_view(request):
    products = Product.objects.all()
    return render(request, "index.html", {"products": products})

# @login_required

# def view_cart(request):
#     # Check if user is authenticated, otherwise use "guest_user"
#     if request.user.is_authenticated:
#         user = request.user
#     else:
#         user, _ = User.objects.get_or_create(username="guest_user")

#     print("Current User:",user.username)  # Debugging

#     # Fetch cart items for the user
#     cart_items = Cart.objects.filter(user=user)

#     # Convert cart items to JSON format
#     cart_data = [
#         {
#             "id": item.id,
#             "product_name": item.product.name,
#             "price": (item.product.price),
#             "quantity": item.quantity,
#             "image_url": item.product.image_url if item.product.image_url else "",  # ✅ Get correct image URL
#         }
#         for item in cart_items
#     ]
#     for item in cart_items:
#         print(f"Product: {item.product.name}, Image URL: {item.product.image_url}")  # ✅ Check if URLs are correct

#     return JsonResponse({"cart_items": cart_data})
def view_cart(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user, _ = User.objects.get_or_create(username="guest_user")

    print("Current User:", user.username)  # Debugging

    # Fetch cart items
    cart_items = Cart.objects.filter(user=user)

    # Convert cart items to JSON format with correct product IDs
    cart_data = [
        {
            "id": item.product.id,  # ✅ Ensure correct Product ID is sent
            "cart_id": item.id,  # ✅ Cart Item ID (in case needed for updates)
            "product_name": item.product.name,
            "price": float(item.product.price),  # Convert Decimal to float
            "quantity": item.quantity,
            "image_url": item.product.image_url if item.product.image_url else "",
        }
        for item in cart_items
    ]

    print("📌 Cart Data Sent to Frontend:", cart_data)  # Debugging

    return JsonResponse({"cart_items": cart_data})



def view_products(request):
    if request.method == 'GET':  # Ensure only GET requests are allowed
        products = Product.objects.all().values("id", "name", "price", "category")  # Fetch all products
        return JsonResponse(list(products), safe=False)  # Convert QuerySet to JSON
    
    return JsonResponse({"error": "Invalid request method"}, status=400)  # Handle non-GET requests



def fetch_products_by_category(request, category):
    products = Product.objects.filter(category=category)
    product_list = list(products.values())
    return JsonResponse({'products': product_list})

def fetch_products_by_subcategory(request, subcategory):
    products = Product.objects.filter(subcategory=subcategory)
    product_list = list(products.values())
    return JsonResponse({'products': product_list})    
    


# Load environment variables
load_dotenv()
@csrf_exempt
def create_payment(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        amount = data.get("amount")
        currency = data.get("currency", "usd")

        if not amount:
            return JsonResponse({"error": "Amount is required"}, status=400)

        #  Load payment gateway details from .env 
        gateway_url = os.getenv("PAYMENT_GATEWAY_URL")  # Generic API endpoint
        api_key = os.getenv("PAYMENT_API_KEY")
        secret_key = os.getenv("PAYMENT_SECRET_KEY")

        if not gateway_url or not api_key or not secret_key:
            return JsonResponse({"error": "Payment gateway credentials missing"}, status=500)

        #  Simulated response for testing 
        if gateway_url == "sandbox":
            return JsonResponse({
                "message": "Sandbox payment successful",
                "transaction_id": "test_txn_123",
                "amount": amount,
                "currency": currency
            })

        # Make a real API request to the gateway 
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "amount": amount,
            "currency": currency,
            "api_key": api_key,
            "secret_key": secret_key
        }

        response = requests.post(gateway_url, json=payload, headers=headers)

        # 🔹 Handle real payment gateway response 🔹
        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({"error": "Payment gateway error", "details": response.text}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON request"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)
