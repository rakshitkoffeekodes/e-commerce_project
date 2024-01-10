import uuid
import stripe
from django.contrib.auth import authenticate
from django.db.models import Max
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import *
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from seller.serilizers import *
from .serlializers import *
from .models import *
from django.contrib.auth.models import User


@api_view(['POST'])
def user_registration(request):
    # Extract data from the request
    user_firstname = request.POST["user_firstname"]
    user_lastname = request.POST["user_lastname"]
    user_email_id = request.POST["user_email_id"]
    user_password = request.POST["user_password"]
    user_confirm_password = request.POST["user_confirm_password"]

    try:
        # Check if the email is already registered
        if User.objects.filter(email=user_email_id).exists():
            return Response({"error": "Email is already registered"}, status=400)

        # Check if the password and confirm_password match
        if user_password == user_confirm_password:
            # Create a new user
            user = User.objects.create_user(
                username=user_email_id.split('@')[0],
                email=user_email_id,
                password=user_password,
                first_name=user_firstname,
                last_name=user_lastname
            )
            user.save()

            # Create a BuyerRegistration instance for the user
            member = BuyerRegistration(buyer=user)
            member.save()

            return Response({"error": "You are successfully Registration in"}, status=200)
        else:
            return Response({"error": "Password and confirm_password do not match"}, status=400)

    except Exception as e:
        return Response({"error": str(e)}, status=404)


@api_view(['POST'])
def user_login(request):
    # Extract data from the request
    user_email_id = request.data["user_email_id"]
    user_password = request.data["user_password"]

    try:
        user = User.objects.get(email=user_email_id)
        if user.check_password(user_password):
            # Authenticate the user
            auth = authenticate(username=user.username, password=user_password)
            if auth is not None:
                # Generate JWT tokens for the user
                refresh = RefreshToken.for_user(auth)
                return Response(
                    {'Message': 'You are successfully logged in', 'refresh': str(refresh),
                     'access': str(refresh.access_token)},
                    status=200)
            else:
                return Response({'Message': 'Invalid username or password.'}, status=400)
        else:
            return Response({"message": "Invalid password"}, status=400)

    except User.DoesNotExist:
        return Response({"error": "Invalid user_email_id"}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def user_profile(request):
    try:
        # Retrieve the authenticated user
        user = request.user
        # Check if the user is authenticated
        if user.is_authenticated:
            # Retrieve the BuyerRegistration instance associated with the user
            buyer_user = BuyerRegistration.objects.get(buyer=user)
            serializer = BuyerRegistrationSerializer(buyer_user)
            serialized_data = serializer.data
            user_data = serialized_data.pop('buyer')
            serialized_data.update(user_data)
            return Response({'data': serialized_data})

        else:
            return Response({"message": "User is not authenticated."}, status=401)

    except BuyerRegistration.DoesNotExist:
        return Response({"error": f"Error in user profile update: {BuyerRegistration.__name__}"}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_update(request):
    # Extract data from the request
    user_firstname = request.POST.get("user_firstname", "")
    user_lastname = request.POST.get("user_lastname", "")
    user_mobile_no = request.POST.get("user_mobile_no", "")
    user_address = request.POST.get("user_address", "")
    user_photo = request.FILES.get("user_photo", "")

    try:
        # Validate mobile number
        if not (user_mobile_no.isdigit() and len(user_mobile_no) == 10):
            return Response({"error": "Invalid mobile number. Please provide a 10-digit number."}, status=400)

        # Check if the mobile number is already registered
        if BuyerRegistration.objects.filter(user_mobile_no=user_mobile_no).exists():
            return Response({"error": "Mobile number is already registered"}, status=400)

        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(buyer=user)

            if user_firstname:
                buyer_user.buyer.first_name = user_firstname
            if user_lastname:
                buyer_user.buyer.last_name = user_lastname
            if user_mobile_no:
                buyer_user.user_mobile_no = user_mobile_no
            if user_address:
                buyer_user.user_address = user_address
            if user_photo:
                buyer_user.user_photo = user_photo

            buyer_user.save()
            serializer = BuyerRegistrationSerializer(buyer_user)
            return Response({"message": "User profile successfully updated.", "data": serializer.data}, status=200)
        else:
            return Response({"message": "User is not authenticated."}, status=401)

    except BuyerRegistration.DoesNotExist:
        return Response({"error": f"Error in user profile update: {BuyerRegistration.__name__}"}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
@api_view(['POST'])
def user_search_product(request):
    # Extract data from the request
    user_search = request.POST["search"]

    try:
        # Filter products based on search criteria
        member = Product.objects.filter(
            Q(product_name__icontains=user_search) |
            Q(product_category__icontains=user_search) |
            Q(product_sub_category__icontains=user_search) |
            Q(product_branding__icontains=user_search) |
            Q(product_size__icontains=user_search) |
            Q(product_color__icontains=user_search) |
            Q(product_fabric__icontains=user_search) |
            Q(product_description__icontains=user_search)
        )

        # If no matching products found, return all products
        if len(member) == 0:
            member = Product.objects.all()
            serializer = ProductSerializer(member, many=True)
        else:
            serializer = ProductSerializer(member, many=True)

        return Response({"message": " user search product successfully .", "data": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
@api_view(['POST'])
def user_view_product():
    try:
        # Retrieve all products
        member = Product.objects.all()
        if len(member) != 0:
            serializer = ProductSerializer(member, many=True)
            return Response({"message": " user view product successfully.", "data": serializer.data}, status=200)
        else:
            return Response({"message": " product is empty ."}, status=400)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_insert_address(request):
    # Extract data from the request
    checkout_street_address = request.POST["street_address"]
    checkout_apartment_address = request.POST["apartment_address"]
    checkout_pincode = request.POST["pincode"]
    checkout_city = request.POST["city"]
    checkout_select_state = request.POST["select_state"]
    checkout_order_receiver_name = request.POST["ord_rec_name"]
    checkout_order_receiver_mobile_no = request.POST["ord_rec_mobile_no"]

    try:
        # Validate pincode
        if not (checkout_pincode.isdigit() and len(checkout_pincode) == 6):
            return Response({"error": "Invalid pincode number. Please provide a 6-digit number."}, status=400)

        # Validate mobile number
        if not (checkout_order_receiver_mobile_no.isdigit() and len(checkout_order_receiver_mobile_no) == 10):
            return Response({"error": "Invalid mobile number. Please provide a 10-digit number."}, status=400)

        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(buyer=user)
            member = Buyer_checkout_details(street_address=checkout_street_address,
                                            apartment_address=checkout_apartment_address,
                                            pincode=checkout_pincode, city=checkout_city,
                                            ord_rec_mobile_no=checkout_order_receiver_mobile_no,
                                            select_state=checkout_select_state,
                                            ord_rec_name=checkout_order_receiver_name,
                                            buyer=buyer_user)
            member.save()
            serializer = BuyerAddressSerializer(member)
            return Response({"message": " user  address successfully insert.", "data": serializer.data}, status=200)

        else:
            return Response({"message": " user is not active"}, status=400)

    except BuyerRegistration.DoesNotExist:
        return Response({"error": f"Error in user address insert: {BuyerRegistration.__name__}"}, status=404)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_view_address(request):
    try:
        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(buyer=user)

            # Get checkout details for the buyer
            member = Buyer_checkout_details.objects.filter(buyer=buyer_user)

            if member.exists():
                serializer = BuyerAddressSerializer(member, many=True)
                return Response({"message": "User addresses successfully viewed.", "data": serializer.data}, status=200)
            else:
                return Response({"message": "Address is empty."}, status=400)
        else:
            return Response({"message": "User is not authenticated."}, status=400)

    except BuyerRegistration.DoesNotExist:
        return Response({"error": f"Error in user address insert: {BuyerRegistration.__name__}"}, status=404)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_update_address(request):
    checkout_address = request.POST["address"]
    checkout_street_address = request.POST.get("street_address")
    checkout_apartment_address = request.POST.get("apartment_address")
    checkout_pincode = request.POST.get("pincode")
    checkout_city = request.POST.get("city")
    checkout_select_state = request.POST.get("select_state")
    checkout_order_receiver_name = request.POST.get("ord_rec_name")
    checkout_order_receiver_mobile_no = request.POST.get("ord_rec_mobile_no")

    try:
        # Validate the address ID
        max_accept_id = Buyer_checkout_details.objects.aggregate(Max('address'))['address__max']
        if not 1 <= int(checkout_address) <= max_accept_id:
            return Response(f"Invalid address. Please provide a valid ID less than or equal to {max_accept_id}.")

        # Validate pincode and mobile number format
        if not (checkout_pincode.isdigit() and len(checkout_pincode) == 6):
            return Response({"error": "Invalid pincode number. Please provide a 6-digit number."}, status=400)
        if not (checkout_order_receiver_mobile_no.isdigit() and len(checkout_order_receiver_mobile_no) == 10):
            return Response({"error": "Invalid mobile number. Please provide a 10-digit number."}, status=400)

        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(buyer=user)
            # Get specific checkout detail based on address and buyer
            member = Buyer_checkout_details.objects.get(address=checkout_address, buyer=buyer_user)
            if not checkout_street_address == '':
                member.street_address = checkout_street_address
            if not checkout_apartment_address == '':
                member.apartment_address = checkout_apartment_address
            if not checkout_pincode == '':
                member.pincode = checkout_pincode
            if not checkout_city == '':
                member.city = checkout_city
            if not checkout_select_state == '':
                member.select_state = checkout_select_state
            if not checkout_order_receiver_name == '':
                member.ord_rec_name = checkout_order_receiver_name
            if not checkout_order_receiver_mobile_no == '':
                member.ord_rec_mobile_no = checkout_order_receiver_mobile_no
            member.save()
            serializer = BuyerAddressSerializer(member)
            return Response({"message": " user  address successfully update.", "data": serializer.data}, status=200)
        else:
            return Response({"message": " user is not active"}, status=400)

    except BuyerRegistration.DoesNotExist:
        return Response({"error": f"Error in user address insert: {BuyerRegistration.__name__}"}, status=404)

    except Buyer_checkout_details.DoesNotExist:
        return Response({"error": f"Error in address profile update: {Buyer_checkout_details.__name__}"}, status=404)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_delete_address(request):
    # Extract data from the request
    checkout_address = request.POST["address"]
    try:
        # Validate address_id
        if not checkout_address or not checkout_address.isdigit():
            return Response({"error": "Invalid or missing address_id. Please provide a valid ID."}, status=400)

        # Validate address_id range
        max_address_id = Buyer_checkout_details.objects.aggregate(Max('address'))['address__max']
        if not 1 <= int(checkout_address) <= max_address_id:
            return Response(f"Invalid address_id. Please provide a valid ID less than or equal to {max_address_id}.",
                            status=400)

        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(buyer=user)
            member = Buyer_checkout_details.objects.get(address=checkout_address, buyer=buyer_user)
            member.delete()

            return Response({"message": "User address successfully deleted."}, status=200)
        else:
            return Response({"message": " user is not active"}, status=400)

    except BuyerRegistration.DoesNotExist:
        return Response({"error": f"Error in user address insert: {BuyerRegistration.__name__}"}, status=404)

    except Buyer_checkout_details.DoesNotExist:
        return Response({"error": f"Error: User profile not found with address_id {Buyer_checkout_details}"},
                        status=404)

    except Exception as e:
        return Response({"error": f"Error: {e}"}, status=500)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_insert_cart(request):
    # Extract data from the request
    cart_product = request.POST['product']
    cart_product_color = request.POST['product_color']
    cart_product_size = request.POST['product_size']

    try:
        # Validate product ID
        max_accept_id = Product.objects.aggregate(Max('id'))['id__max']
        if not 1 <= int(cart_product) <= max_accept_id:
            return Response(f"Invalid product. Please provide a valid ID less than or equal to {max_accept_id}.")

        # Get product details based on the product ID
        product_value = Product.objects.get(id=cart_product)
        if product_value == "":
            return Response({"error": "Product is empty ."}, status=400)

        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(buyer=user)
            # Create a new BuyerCart instance with product details
            member = BuyerCart(qty=1, product_color=cart_product_color, product_size=cart_product_size,
                               total=product_value.product_price,
                               buyer=buyer_user, product=product_value)
            member.save()
            serializer = BuyerCartSerializer(member)
            return Response({"message": " user cart successfully insert .", "data": serializer.data}, status=200)
        else:
            return Response({"message": " user is not active"}, status=400)

    except Product.DoesNotExist:
        return Response({"error": f"Error in  cart  insert: {Product.__name__}"}, status=404)

    except BuyerRegistration.DoesNotExist:
        return Response({"error": f"Error in user address insert: {BuyerRegistration.__name__}"}, status=404)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_view_cart(request):
    try:
        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(buyer=user)
            # Get all cart items for the buyer
            member = BuyerCart.objects.filter(buyer=buyer_user)
            if member != "":
                serializer = BuyerCartSerializer(member, many=True)
                return Response({"message": " user cart successfully view .", "data": serializer.data}, status=200)
            else:
                return Response({"message": " address is empty ."}, status=400)
        else:
            return Response({"message": " user is not active"}, status=400)

    except BuyerRegistration.DoesNotExist:
        return Response({"error": f"Error in  cart  view: {Product.__name__}"}, status=404)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_update_cart(request):
    # Extract data from the request
    user_cart = request.POST['cart']
    cart_qty = request.POST.get('qty')
    cart_product_color = request.POST.get('product_color')
    cart_product_size = request.POST.get('product_size')

    try:
        # Validate quantity
        if not 1 <= int(cart_qty) <= 100 and (cart_qty.isdigit()):
            return Response({"message": "Invalid qty number. Qty should be between 1 and 100."}, status=400)

        # Validate cart ID
        max_address_id = Buyer_checkout_details.objects.aggregate(Max('cart'))['cart__max']
        if not 1 <= int(user_cart) <= max_address_id:
            return Response(f"Invalid cart. Please provide a valid ID less than or equal to {max_address_id}.",
                            status=400)
        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(buyer=user)
            # Get specific cart item based on cart ID and buyer
            member = BuyerCart.objects.get(pk=user_cart, buyer=buyer_user)
            # Calculate total based on quantity
            total = int(cart_qty) * member.total

            if not member == "":
                if not cart_qty == '':
                    member.qty = cart_qty
                if not cart_product_color == '':
                    member.product_color = cart_product_color
                if not cart_product_size == '':
                    member.product_size = cart_product_size
                if not total == '':
                    member.total = total
                member.save()
                serializer = BuyerCartSerializer(member)
                return Response({"message": " user cart successfully update.", "data": serializer.data}, status=200)
            else:
                return Response({"message": " cart is empty ."}, status=400)
        else:
            return Response({"message": " user is not active"}, status=400)

    except BuyerRegistration.DoesNotExist:
        return Response({"error": f"Error in  cart  Update: {Product.__name__}"}, status=404)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_delete_cart(request):
    # Extract data from the request
    user_cart = request.POST['cart']
    try:
        # Validate cart ID
        max_address_id = BuyerCart.objects.aggregate(Max('cart'))['cart__max']
        if not 1 <= int(user_cart) <= max_address_id:
            return Response(f"Invalid cart. Please provide a valid ID less than or equal to {max_address_id}.",
                            status=400)
        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(buyer=user)
            # Get specific cart item based on cart ID and buyer
            member = BuyerCart.objects.get(pk=user_cart, buyer=buyer_user)
            member.delete()
            return Response({"message": " user cart successfully deleted."}, status=200)
        else:
            return Response({"message": " user is not active"}, status=400)

    except BuyerRegistration.DoesNotExist:
        return Response({"error": f"Error in  cart  delete: {Product.__name__}"}, status=404)

    except Buyer_checkout_details.DoesNotExist:
        return Response({"error": f"user Invalid id select {Buyer_checkout_details.__name__}"}, status=404)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_insert_buynow(request):
    # Extract data from the request
    user_product = request.POST['product']
    user_checkout = request.POST['Checkout']
    qty = request.POST['qty']
    try:
        # Validate quantity, product ID, and Checkout ID
        max_address_id = Buyer_checkout_details.objects.aggregate(Max('address'))['address__max']
        max_product_id = Product.objects.aggregate(Max('id'))['id__max']

        if not 1 <= int(qty) <= 100 or not qty.isdigit():
            return Response({"error": "Invalid qty number. Qty should be between 1 and 100."}, status=400)

        if not 1 <= int(user_product) <= max_product_id:
            return Response(f"Invalid product. Please provide a valid ID less than or equal to {max_product_id}.",
                            status=400)

        if not 1 <= int(user_checkout) <= max_address_id:
            return Response(f"Invalid Checkout. Please provide a valid ID less than or equal to {max_address_id}.",
                            status=400)

        # buyer_user = BuyerRegistration.objects.get(user_email_id=request.session['user_email_id'])
        product_data = Product.objects.get(id=user_product)
        checkout_data = Buyer_checkout_details.objects.get(address=user_checkout)
        total = int(qty) * product_data.product_price

        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(buyer=user)
            # Create a new record in BuyerPurchase
            member = BuyerPurchase(qty=qty, total=total, buyer=buyer_user, product=product_data, checkout=checkout_data)
            member.save()

            serializer = BuyercartPurchaseSerializer(member)
            return Response({"message": "User buy the product successfully.", "data": serializer.data}, status=200)
        else:
            return Response({"message": " user is not active"}, status=400)

    except BuyerRegistration.DoesNotExist:
        return Response({"error": "Buyer not found."}, status=404)

    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=404)

    except Buyer_checkout_details.DoesNotExist:
        return Response({"error": "Checkout details not found."}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_insert_cart_buynow(request):
    # Extract data from the request
    user_cart = request.POST['cart']
    user_checkout = request.POST['Checkout']

    try:
        # Validate cart ID and checkout address
        max_address_id = Buyer_checkout_details.objects.aggregate(Max('address'))['address__max']
        max_card_id = BuyerCart.objects.aggregate(Max('Cart'))['Cart__max']

        if not 1 <= int(user_cart) <= max_card_id:
            return Response(f"Invalid card. Please provide a valid ID less than or equal to {max_card_id}.",
                            status=400)

        if not 1 <= int(user_checkout) <= max_address_id:
            return Response(f"Invalid Checkout. Please provide a valid ID less than or equal to {max_address_id}.",
                            status=400)
        # Get cart and checkout details based on provided IDs
        cart = BuyerCart.objects.get(pk=user_cart)
        checkout = Buyer_checkout_details.objects.get(address=user_checkout)
        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(buyer=user)
            # Create a new record in BuyerPurchase using cart and checkout details
            member = BuyerPurchase(
                qty=cart.qty, total=cart.total, buyer=buyer_user,
                product=cart.product, cart=cart, checkout=checkout
            )
            member.save()
            serializer = BuyercartPurchaseSerializer(member)
            return Response({"message": " user cart to buy  Product successfully .", "data": serializer.data},
                            status=200)
        else:
            return Response({"message": " user is not active"}, status=400)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


# Create a payment intent for the purchase
stripe.api_key = 'sk_test_51OU5FMSAvmPjZJjlUaHxMRIUgI3enoGyrOyvGh1LP5OOl7UuUDZxkJemUPCCi6hWVZ2yWyxU7ADIe7tsN5wVdHVN00D0dS4gP0'


@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_payment_intent(request):
    # Extract data from the request
    user_purchase = request.POST['purchase_data']
    try:
        # Validate purchase data Id
        max_purchase_id = BuyerPurchase.objects.aggregate(Max('purchase'))['purchase__max']
        if not user_purchase.isdigit() or not 1 <= int(user_purchase) <= max_purchase_id:
            return Response(
                {"error": f"Invalid purchase_data. Please provide a valid ID less than or equal to {max_purchase_id}."},
                status=400)

        unique_id = str(uuid.uuid4().int)[:9]
        order_id = "ORD" + unique_id
        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(buyer=user)
            details = BuyerPurchase.objects.get(pk=user_purchase)
            # Create a payment intent using Stripe API
            intent = stripe.PaymentIntent.create(
                amount=details.total,
                currency='inr',
            )
            # Create a payment record in BuyerPayment
            payment = BuyerPayment.objects.create(
                amount=details.total,
                currency='INR',
                status='Success',
                payment_intent_id=intent.id,
                details=details,
                buyer=buyer_user,
                order=order_id
            )

            serializer = BuyerPaymentSerializer(payment)
            return Response({"message": "User payment successfully.", "data": serializer.data}, status=200)

        else:
            return Response({"message": " user is not active"}, status=400)

    except BuyerPurchase.DoesNotExist:
        print("Invalid purchase id. Please select a valid purchase id.")

    except Exception as e:
        return Response({"error": str(e)}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_conform_order(request):
    try:
        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(buyer=user)
            # Retrieve the latest Accept record for the buyer
            accept = Accept.objects.filter(buyer=buyer_user).latest('id')

            if not accept == "":
                return Response({"message": "  Conform Order successfully ."}, status=200)
            else:
                return Response({"message": "Cancel  your Order "}, status=200)

        else:
            return Response({"message": " user is not active"}, status=400)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_insert_feedback(request):
    # Extract data from the request
    feedback_description = request.POST['feedback_description']
    feedback_rating = request.POST['feedback_rating']
    feedback_photo = request.FILES['feedback_photo']
    feedback_product = request.POST['feedback_product']
    try:
        # Validate the product ID
        max_accept_id = Product.objects.aggregate(Max('id'))['id__max']
        if not 1 <= int(feedback_product) <= max_accept_id:
            return Response(f"Invalid product. Please provide a valid ID less than or equal to {max_accept_id}.")

        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(buyer=user)
            product_data = Product.objects.get(id=feedback_product)
            if not product_data == "":
                # Create a new BuyerFeedback record
                member = BuyerFeedback(
                    feedback_description=feedback_description,
                    feedback_rating=feedback_rating,
                    feedback_photo=feedback_photo,
                    feedback_product=product_data,
                    feedback_login=buyer_user,
                )
                print(member)
                member.save()
                serializer = BuyerFeedbackSerializer(member)
                return Response({"message": " user feedback successfully insert .", "data": serializer.data},
                                status=200)
            else:
                return Response({"message": " product is empty ."}, status=400)

        else:
            return Response({"message": " user is not active"}, status=400)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
@api_view(['POST'])
def user_view_feedback():
    try:
        # Retrieve all BuyerFeedback records
        member = BuyerFeedback.objects.all()
        if not member == "":
            serializer = BuyerFeedbackSerializer(member, many=True)
            return Response({"message": " user feedback successfully view .", "data": serializer.data}, status=200)
        else:
            return Response({"message": " product is empty ."}, status=400)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
@api_view(['POST'])
def user_filter_product(request):
    # Extract data from the request
    product_size = request.POST.get('product_size', "")
    product_color = request.POST.get('product_color', "")
    product_branding = request.POST.get('product_branding', "")
    min_product_price = request.POST.get('min_product_price', 0)
    max_product_price = request.POST.get('max_product_price', 100000)
    max_product_rating = request.POST.get('max_product_rating', 5)

    try:
        # Apply filters based on available parameters
        if product_color != '' and product_size != '' and product_branding != '' and max_product_price != '':
            products = Product.objects.filter(
                product_size=product_size,
                product_color=product_color,
                product_branding=product_branding,
                product_price__range=(min_product_price, max_product_price),
                buyerfeedback__feedback_rating=max_product_rating).distinct()
            if products == "":
                return Response({"message": " product is empty ."}, status=400)

        elif product_size != '':
            products = Product.objects.filter(product_size=product_size)
        elif product_color != '':
            products = Product.objects.filter(product_color=product_color)
        elif product_branding != '':
            products = Product.objects.filter(product_branding=product_branding)
        elif max_product_price != '':
            products = Product.objects.filter(product_price__range=(min_product_price, max_product_price))
        elif max_product_rating != '':
            products = Product.objects.filter(buyerfeedback__feedback_rating=max_product_rating)

        serializer = ProductSerializer(products, many=True)
        return Response({"message": " user filter  Product successfully view.", "data": serializer.data}, status=200)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_view_order(request):
    try:
        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(buyer=user)
            # Retrieve the orders for the buyer user
            accept = Accept.objects.filter(buyer=buyer_user)
            if not accept == "":
                serializer = AcceptSerializer(accept, many=True)
                return Response({"message": "User payment successfully.", "data": serializer.data}, status=200)

            else:
                return Response({"message": " order is empty ."}, status=400)
        else:
            return Response({"message": " user is not active"}, status=400)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_cancel_order(request):
    # Extract data from the request
    order_id = request.POST['order_id']
    try:
        # Get the payment record associated with the order_id
        accept = BuyerPayment.objects.get(order=order_id)
        accept.cancel = False
        accept.save()

        serializer = BuyerPaymentSerializer(accept)
        return Response({"message": "User payment successfully.", "data": serializer.data}, status=200)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_return_order(request):
    # Extract data from the request
    user_accept = request.POST['accept_id']
    order_return_message = request.POST['order_return_message']
    try:
        # Check if the accept_id is valid
        max_accept_id = Accept.objects.aggregate(Max('id'))['id__max']
        if not 1 <= int(user_accept) <= max_accept_id:
            return Response(f"Invalid accept_id. Please provide a valid ID less than or equal to {max_accept_id}.")

        # Generate a unique order return ID
        unique_id = str(uuid.uuid4().int)[:9]
        order_id = "RET" + unique_id

        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(buyer=user)
            # Get the accept and payment instances
            accept_instance = Accept.objects.get(id=user_accept, buyer=buyer_user)
            buyer_payment_instance = BuyerPayment.objects.get(order=accept_instance.order)

            if not accept_instance == "" or buyer_payment_instance == "":
                # Create a Return instance
                return_instance = Return(
                    buyer=buyer_user,
                    order=buyer_payment_instance,
                    returns=order_id,
                    order_return_message=order_return_message,
                    return_shipping_Fee=100,  # Adjust the value as needed
                    return_date=datetime.now(),
                    status=True
                )
                return_instance.save()

                serializer = ReturnSerializer(return_instance)
                return Response({"message": "User return successfully.", "data": serializer.data}, status=200)

            else:
                return Response({"message": " data   is empty ."}, status=200)

        else:
            return Response({"message": " user is not active"}, status=400)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_view_return(request):
    try:
        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(buyer=user)
            # Retrieve the returns for the buyer user
            member = Return.objects.filter(buyer=buyer_user)
            print(member)
            if not member == "":
                serializer = ReturnSerializer(member, many=True)
                return Response({"message": " user Return successfully view .", "data": serializer.data}, status=200)
            else:
                return Response({"message": " Return is empty ."}, status=400)
        else:
            return Response({"message": " user is not active"}, status=400)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
@api_view(['POST'])
def user_view_product_clothe():
    try:
        # Filter products based on category and sub-category
        buyer_user = Product.objects.filter(product_category="ELECTRONICS", product_sub_category="HOME AUDIO")

        if not buyer_user == "":

            serializer = ProductSerializer(buyer_user, many=True)
            return Response({"message": " user view product successfully.", "data": serializer.data}, status=200)
        else:
            return Response({"message": " product is empty ."}, status=400)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)
