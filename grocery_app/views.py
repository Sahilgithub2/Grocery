from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from grocery_app.forms import CaptchaForm

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
from grocery_app.forms import CaptchaForm

def sign_up_view(request):
    if request.method == 'POST':
        form = CaptchaForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            # Additional user fields can be added here

            # Create a new user
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Account created successfully!')
            return redirect('index')  # Redirect to the index or login page
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = CaptchaForm()

    return render(request, 'sign_up.html', {'form': form})

# Create your views here.
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
                'image_url': image_url,
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

@csrf_exempt  # Disable CSRF for testing (not recommended in production)
def add_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Read JSON from request
            product_id = data.get('product_id')

            if not product_id:
                return JsonResponse({"error": "Product ID is required"}, status=400)

            product = Product.objects.get(id=product_id)  # Fetch product

            if request.user.is_authenticated:
                user = request.user  # ✅ Use the logged-in user
            else:
                return JsonResponse({"error": "User not authenticated"}, status=401)

            # Add product to cart for the authenticated user
            cart_item, created = Cart.objects.get_or_create(user=user, product=product)
            if not created:
                cart_item.quantity += 1
            cart_item.save()

            return JsonResponse({
                "message": "Product added to cart",
                "product": product.name,
                "quantity": cart_item.quantity
            })

        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt  # Disable CSRF for testing (NOT recommended for production)
def remove_from_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Read JSON from request
            product_id = data.get('product_id')

            if not product_id:
                return JsonResponse({"error": "Product ID is required"}, status=400)

            try:
                product = Product.objects.get(id=product_id)  # Fetch product
            except Product.DoesNotExist:
                return JsonResponse({"error": "Product not found"}, status=404)

            if not request.user.is_authenticated:
                return JsonResponse({"error": "User not authenticated"}, status=401)

            user = request.user  # ✅ Use the logged-in user

            try:
                cart_item = Cart.objects.get(user=user, product=product)
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                    quantity = cart_item.quantity  # ✅ Safe reference after save()
                else:
                    cart_item.delete()
                    quantity = 0  # ✅ Avoid referencing deleted object

                return JsonResponse({
                    "message": "Product removed from cart",
                    "product": product.name,
                    "quantity": quantity  # ✅ Ensure valid quantity reference
                })

            except Cart.DoesNotExist:
                return JsonResponse({"error": "Product not in cart"}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def index_view(request):
    products = Product.objects.all()
    return render(request, "index.html", {"products": products})

#@login_required

def view_cart(request):
    # Check if user is authenticated, otherwise use "guest_user"
    if request.user.is_authenticated:
        user = request.user
    else:
        user, _ = User.objects.get_or_create(username="guest_user")

    print("Current User:", user.username)  # Debugging

    # Fetch cart items for the user
    cart_items = Cart.objects.filter(user=user)

    # Convert cart items to JSON format
    cart_data = [
        {
            "id": item.id,
            "product_name": item.product.name,
            "price": item.product.price,
            "quantity": item.quantity,
            "image_url": item.product.image_url,
        }
        for item in cart_items
    ]
    
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