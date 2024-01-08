from rest_framework.response import Response
from .serlializers import *
from .models import *
from rest_framework import status
from rest_framework.decorators import *
from django.contrib.auth.models import User
from seller.models import *
from seller.serilizers import *
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import uuid
from django.db.models import Max
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication




@api_view(['POST'])
def user_registration(request):
    user_firstname = request.POST["user_firstname"]
    user_lastname = request.POST["user_lastname"]
    user_email_id = request.POST["user_email_id"]
    user_password = request.POST["user_password"]
    user_confirm_password = request.POST["user_confirm_password"]

    try:

    # if User.objects.filter(user_email_id=user_email_id).exists():
    #     return Response({"error": "Email is already registered"}, status=400)

        if user_password == user_confirm_password:
            print("yes")
            user = User.objects.create_user(username=user_email_id.split('@')[0],
                                            email=user_email_id,
                                            password=user_password,
                                            first_name=user_firstname,last_name=user_lastname)
            user.save()
            member = BuyerRegistration(buyer=user)
            member.save()

            return Response({"error": "You are successfully Registration in"}, status=200)
        else:
            return Response({"error": "Password and confirm_password do not match"}, status=400)

    except Exception as e:
        return Response({"error": str(e)}, status=404)

@api_view(['POST'])
def user_login(request):
    user_email_id = request.data.get("user_email_id")  # Use request.data for POST data
    user_password = request.data.get("user_password")

    try:
        user = User.objects.get(email=user_email_id)
        if user.check_password(user_password):
            auth = authenticate(username=user.username, password=user_password)
            if auth is not None:
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
@api_view(['POST'])
def user_profile(request):
    try:
        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(buyer=user)

            # path = request.META['HTTP_HOST']
            # path1 = 'http://' + path + '/media/' + str(buyer_user.user_photo)
            # buyer_user.user_photo = path1

            serializer = RegisterSerializer(buyer_user)
            print(serializer)

            return Response({"message": "User profile retrieved successfully.", "data": serializer.data}, status=200)
        else:
            return Response({"message": "User is not authenticated."}, status=401)

    except User.DoesNotExist:
        return Response({"error": "User matching query does not exist."}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    # try:
    # user = request.user
    # print(user)
    # if user.is_authenticated:
    #     # buyer_user = BuyerRegistration.objects.get(user_id=user.id)
    #     buyer_user = User.objects.get(email=user.id)
    #     print(buyer_user)
    #
    #     path = request.META['HTTP_HOST']
    #
    #     path1 = 'http://' + path + '/media/' + str(buyer_user.user_photo)
    #     buyer_user.user_photo = path1
    #
    #     serializer = RegisterSerializer(buyer_user)
    #     return Response({"message": " user profile successfully view.", "data": serializer.data}, status=200)
    # else:
    #     return Response({"message": " user is not active"}, status=400)

    # except BuyerRegistration.DoesNotExist:
    #     return Response("BuyerRegistration not found for the user.", status=404)
    # except Exception as e:
    #     return Response({"error": e.__str__()}, status=404)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_update(request):
    user_firstname = request.POST.get("user_firstname", "")
    user_lastname = request.POST.get("user_lastname", "")
    user_mobile_no = request.POST.get("user_mobile_no", "")
    user_address = request.POST.get("user_address", "")
    user_photo = request.FILES.get("user_photo", "")

    try:
        if not (user_mobile_no.isdigit() and len(user_mobile_no) == 10):
            return Response({"error": "Invalid mobile number. Please provide a 10-digit number."}, status=400)

        if BuyerRegistration.objects.filter(user_mobile_no=user_mobile_no).exists():
            return Response({"error": "Mobile number is already registered"}, status=400)

        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(user_id=user.id)

            if user_firstname:
                buyer_user.user_firstname = user_firstname
            if user_lastname:
                buyer_user.user_lastname = user_lastname
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
            return Response({"message": " user is not active"}, status=400)


    except BuyerRegistration.DoesNotExist:
        return Response({"error": f"Error in user profile update: {BuyerRegistration.__name__}"}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
@authentication_classes([JWTAuthentication])
@permission_classes([ AllowAny])
@api_view(['POST'])
def user_search_product(request):
    search = request.POST["search"]

    try:
        member = Product.objects.filter(
            Q(product_name__icontains=search) |
            Q(product_category__icontains=search) |
            Q(product_sub_category__icontains=search) |
            Q(product_branding__icontains=search) |
            Q(product_size__icontains=search) |
            Q(product_color__icontains=search) |
            Q(product_fabric__icontains=search) |
            Q(product_description__icontains=search)
        )


        if len(member)==0:
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
def user_view_product(request):
    try:

        buyer_user = Product.objects.all()
        if len(buyer_user)!=0:
            serializer = ProductSerializer(buyer_user, many=True)
            return Response({"message": " user view product successfully.", "data": serializer.data}, status=200)
        else:
            return Response({"message": " product is empty ."}, status=400)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_insert_address(request):
    street_address = request.POST["street_address"]
    apartment_address = request.POST["apartment_address"]
    pincode = request.POST["pincode"]
    city = request.POST["city"]
    select_state = request.POST["select_state"]
    ord_rec_name = request.POST["ord_rec_name"]
    ord_rec_mobile_no = request.POST["ord_rec_mobile_no"]

    try:
        if not (pincode.isdigit() and len(pincode) == 6):
            return Response({"error": "Invalid pincode number. Please provide a 6-digit number."}, status=400)

        if not (ord_rec_mobile_no.isdigit() and len(ord_rec_mobile_no) == 10):
            return Response({"error": "Invalid mobile number. Please provide a 10-digit number."}, status=400)
        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(user_id=user.id)
            member = Checkout_details(street_address=street_address, apartment_address=apartment_address,
                                      pincode=pincode, city=city, ord_rec_mobile_no=ord_rec_mobile_no,
                                      select_state=select_state, ord_rec_name=ord_rec_name,buyer=buyer_user)
            member.save()
            serializer = BuyerAddressSerializer(member)
            return Response({"message": " user  address successfully insert.", "data": serializer.data}, status=200)

        else:
            return Response({"message": " user is not active"}, status=400)


    except Exception as e:
        return Response({"error": e.__str__()}, status=404)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_view_address(request):
    try:
        user = request.user
        if user.is_authenticated:
            member = Checkout_details.objects.filter(buyer=user.id)
            if member !="":
                serializer = BuyerAddressSerializer(member, many=True)
                return Response({"message": " user  address successfully view.", "data": serializer.data}, status=200)
            else:
                return Response({"message": " address is empty ."}, status=400)
        else:
            return Response({"message": " user is not active"}, status=400)


    except Exception as e:
        return Response({"error": e.__str__()}, status=404)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_update_address(request):
    address = request.POST["address"]
    street_address = request.POST.get("street_address")
    apartment_address = request.POST.get("apartment_address")
    pincode = request.POST.get("pincode")
    city = request.POST.get("city")
    select_state = request.POST.get("select_state")
    ord_rec_name = request.POST.get("ord_rec_name")
    ord_rec_mobile_no = request.POST.get("ord_rec_mobile_no")


    try:
        max_accept_id = Checkout_details.objects.aggregate(Max('address'))['address__max']
        if not 1 <= int(address) <= max_accept_id:
            return Response(f"Invalid address. Please provide a valid ID less than or equal to {max_accept_id}.")

        if not (pincode.isdigit() and len(pincode) == 6):
            return Response({"error": "Invalid pincode number. Please provide a 6-digit number."}, status=400)

        if not (ord_rec_mobile_no.isdigit() and len(ord_rec_mobile_no) == 10):
            return Response({"error": "Invalid mobile number. Please provide a 10-digit number."}, status=400)
        user = request.user
        if user.is_authenticated:
            member = Checkout_details.objects.get(address=address,buyer=user.id)
            if not street_address == '':
                member.street_address = street_address
            if not apartment_address == '':
                member.apartment_address = apartment_address
            if not pincode == '':
                member.pincode = pincode
            if not city == '':
                member.city = city
            if not select_state == '':
                member.select_state = select_state
            if not ord_rec_name == '':
                member.ord_rec_name = ord_rec_name
            if not ord_rec_mobile_no == '':
                member.ord_rec_mobile_no = ord_rec_mobile_no
            member.save()
            serializer = BuyerAddressSerializer(member)
            return Response({"message": " user  address successfully update.", "data": serializer.data}, status=200)
        else:
            return Response({"message": " user is not active"}, status=400)


    except Exception as e:
        return Response({"error": e.__str__()}, status=404)

    except Checkout_details.DoesNotExist:
        return Response({"error": f"Error in address profile update: {Checkout_details.__name__}"}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_delete_address(request):
    try:
        address_id = request.POST["address_id"]

        if not address_id or not address_id.isdigit():
            return Response({"error": "Invalid or missing address_id. Please provide a valid ID."}, status=400)

        max_address_id = Checkout_details.objects.aggregate(Max('address'))['address__max']

        if not 1 <=int(address_id) <= max_address_id:
            return Response(f"Invalid address_id. Please provide a valid ID less than or equal to {max_address_id}.",status=400)

        user = request.user
        if user.is_authenticated:
            member = Checkout_details.objects.get(address=address_id, buyer=user.id)
            member.delete()

            return Response({"message": "User profile successfully deleted."}, status=200)
        else:
            return Response({"message": " user is not active"}, status=400)


    except Checkout_details.DoesNotExist:
        return Response({"error": f"Error: User profile not found with address_id {address_id}"}, status=404)

    except Exception as e:
        return Response({"error": f"Error: {e}"}, status=500)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_insert_cart(request):
    product_color = request.POST['product_color']
    product_size = request.POST['product_size']
    product = request.POST['product']
    try:
        max_accept_id = Product.objects.aggregate(Max('id'))['id__max']
        if not 1 <= int(product) <= max_accept_id:
            return Response(f"Invalid product. Please provide a valid ID less than or equal to {max_accept_id}.")

        product_value = Product.objects.get(id=product)
        if  product_value=="":
            return Response({"error": "Product is empty ."}, status=400)

        user = request.user
        if user.is_authenticated:

            buyer_user = BuyerRegistration.objects.get(user_email_id=user)
            member = BuyerCart(qty=1, product_color=product_color, product_size=product_size, total=product_value.product_price,
                               buyer=buyer_user, product=product_value)
            member.save()
            serializer = BuyerCartSerializer(member)
            return Response({"message": " user cart successfully insert .", "data": serializer.data}, status=200)
        else:
            return Response({"message": " user is not active"}, status=400)


    except Exception as e:
        return Response({"error": e.__str__()}, status=404)

    except Product.DoesNotExist:
        return Response({"error": f"Error in  cart  insert: {Product.__name__}"}, status=404)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_view_cart(request):

    try:
        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(user_email_id=user)
            member = BuyerCart.objects.filter(buyer=buyer_user)
            if member != "":
                serializer = BuyerCartSerializer(member, many=True)
                return Response({"message": " user cart successfully view .", "data": serializer.data}, status=200)
            else:
                return Response({"message": " address is empty ."}, status=400)
        else:
            return Response({"message": " user is not active"}, status=400)

    except BuyerRegistration.DoesNotExist:
        return Response({"error": f"Error in  cart  insert: {Product.__name__}"}, status=404)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_update_cart(request):
    cart = request.POST['cart']
    qty = request.POST.get('qty')
    product_color = request.POST.get('product_color')
    product_size = request.POST.get('product_size')

    try:

        if not 1 <= int(qty) <= 100 and (qty.isdigit()):
            return Response({"message": "Invalid qty number. Qty should be between 1 and 100."}, status=400)

        max_address_id = Checkout_details.objects.aggregate(Max('address'))['address__max']
        if not 1 <= int(cart) <= max_address_id:
            return Response(f"Invalid cart. Please provide a valid ID less than or equal to {max_address_id}.", status=400)
        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(user_email_id=user)
            member = BuyerCart.objects.get(pk=cart,buyer=buyer_user)

            total = int(qty) * member.total

            if not member=="":
                if not qty == '':
                    member.qty = qty
                if not product_color == '':
                    member.product_color = product_color
                if not product_size == '':
                    member.product_size = product_size
                if not total == '':
                    member.total = total
                member.save()
                serializer = BuyerCartSerializer(member)
                return Response({"message": " user cart successfully update.", "data": serializer.data}, status=200)
            else:
                return Response({"message": " cart is empty ."}, status=400)
        else:
            return Response({"message": " user is not active"}, status=400)
    except Exception as e:
        return Response({"error": e.__str__()}, status=404)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_delete_cart(request):
    cart = request.POST['cart']
    try:

        max_address_id = Checkout_details.objects.aggregate(Max('address'))['address__max']
        if not 1 <= int(cart) <= max_address_id:
            return Response(f"Invalid cart. Please provide a valid ID less than or equal to {max_address_id}.",status=400)
        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(user_email_id=user)

            member = BuyerCart.objects.get(pk=cart,buyer=buyer_user)
            member.delete()
            return Response({"message": " user cart successfully deleted."}, status=200)
        else:
            return Response({"message": " user is not active"}, status=400)

    except Checkout_details.DoesNotExist:
        return Response({"error": f"user Invalid id select {Checkout_details.__name__}"}, status=404)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_insert_buynow(request):
    qty = request.POST['qty']
    product_id = request.POST['product']
    Checkout_id = request.POST['Checkout']
    try:

        max_address_id = Checkout_details.objects.aggregate(Max('address'))['address__max']
        max_product_id = Product.objects.aggregate(Max('id'))['id__max']

        if not 1 <= int(qty) <= 100 or not qty.isdigit():
            return Response({"error": "Invalid qty number. Qty should be between 1 and 100."}, status=400)

        if not 1 <= int(product_id) <= max_product_id:
            return Response(f"Invalid product. Please provide a valid ID less than or equal to {max_product_id}.",
                            status=400)

        if not 1 <= int(Checkout_id) <= max_address_id:
            return Response(f"Invalid Checkout. Please provide a valid ID less than or equal to {max_address_id}.",
                            status=400)

        # buyer_user = BuyerRegistration.objects.get(user_email_id=request.session['user_email_id'])
        product_data = Product.objects.get(id=product_id)
        checkout_data = Checkout_details.objects.get(address=Checkout_id)
        total = int(qty) * product_data.product_price

        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(user_email_id=user)

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

    except Checkout_details.DoesNotExist:
        return Response({"error": "Checkout details not found."}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_insert_cart_buynow(request):
    cart_id = request.POST['cart']
    checkout_address = request.POST['Checkout']

    try:

        max_address_id = Checkout_details.objects.aggregate(Max('address'))['address__max']
        max_card_id = BuyerCart.objects.aggregate(Max('id'))['id__max']

        if not 1 <= int(cart_id) <= max_card_id:
            return Response(f"Invalid card. Please provide a valid ID less than or equal to {max_card_id}.",
                            status=400)

        if not 1 <= int(checkout_address) <= max_address_id:
            return Response(f"Invalid Checkout. Please provide a valid ID less than or equal to {max_address_id}.",
                            status=400)

        # buyer_user = BuyerRegistration.objects.get(user_email_id=request.session['user_email_id'])
        cart = BuyerCart.objects.get(id=cart_id)
        checkout = Checkout_details.objects.get(address=checkout_address)
        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(user_email_id=user)

            member = BuyerPurchase(
                qty=cart.qty, total=cart.total, buyer=buyer_user,
                product=cart.product, cart=cart, checkout=checkout
            )
            member.save()
            serializer = BuyercartPurchaseSerializer(member)
            return Response({"message": " user cart to buy  Product successfully .", "data": serializer.data}, status=200)
        else:
            return Response({"message": " user is not active"}, status=400)


    except Exception as e:
        return Response({"error": e.__str__()}, status=404)



stripe.api_key = 'sk_test_51OU5FMSAvmPjZJjlUaHxMRIUgI3enoGyrOyvGh1LP5OOl7UuUDZxkJemUPCCi6hWVZ2yWyxU7ADIe7tsN5wVdHVN00D0dS4gP0'


@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_payment_intent(request):
    purchase_data = request.POST.get('purchase_data')
    try:

        max_purchase_id = BuyerPurchase.objects.aggregate(Max('id'))['id__max']
        if not purchase_data.isdigit() or not 1 <= int(purchase_data) <= max_purchase_id:
            return Response({"error": f"Invalid purchase_data. Please provide a valid ID less than or equal to {max_purchase_id}."},status=400)

        unique_id = str(uuid.uuid4().int)[:9]
        order_id = "ORD" + unique_id
        # buyer_user = BuyerRegistration.objects.get(user_email_id=request.session.get('user_email_id'))
        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(user_email_id=user)
            details = BuyerPurchase.objects.get(id=purchase_data)
            intent = stripe.PaymentIntent.create(
                amount=details.total,
                currency='inr',
            )

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
def user_Conform_order(request):
    try:
        # buyer_user = BuyerRegistration.objects.get(user_email_id=request.session['user_email_id'])
        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(user_email_id=user)
            accept = Accept.objects.filter(buyer=buyer_user).latest('id')

            if not accept=="":
                return  Response({"message": "  Conform Order successfully ."}, status=200)
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
    feedback_description = request.POST['feedback_description']
    feedback_rating = request.POST['feedback_rating']
    feedback_photo = request.FILES['feedback_photo']
    feedback_product = request.POST['feedback_product']
    try:

        max_accept_id = Product.objects.aggregate(Max('id'))['id__max']
        if not 1 <= int(feedback_product) <= max_accept_id:
            return Response(f"Invalid product. Please provide a valid ID less than or equal to {max_accept_id}.")

        # buyer_user = BuyerRegistration.objects.get(user_email_id=request.session['user_email_id'])
        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(user_email_id=user)
            product_data = Product.objects.get(id=feedback_product)
            if not product_data =="":
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
                return Response({"message": " user feedback successfully insert .", "data": serializer.data}, status=200)
            else:
                return Response({"message": " product is empty ."}, status=400)

        else:
            return Response({"message": " user is not active"}, status=400)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)

@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
@api_view(['POST'])
def user_view_feedback(request):
    try:

        member = BuyerFeedback.objects.all()
        if not member=="":
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
    product_size = request.POST.get('product_size', "")
    product_color = request.POST.get('product_color', "")
    product_branding = request.POST.get('product_branding', "")
    min_product_price = request.POST.get('min_product_price', 0)
    max_product_price = request.POST.get('max_product_price', 100000)
    max_product_rating = request.POST.get('max_product_rating', 5)

    try:

        if product_color != '' and product_size != '' and product_branding != '' and max_product_price != '':
            products = Product.objects.filter(
                product_size=product_size,
                product_color=product_color,
                product_branding=product_branding,
                product_price__range=(min_product_price, max_product_price),
                buyerfeedback__feedback_rating=max_product_rating).distinct()
            if products=="":
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
            buyer_user = BuyerRegistration.objects.get(user_email_id=user)
            accept = Accept.objects.filter(buyer=buyer_user)
            if not accept=="":
                serializer = AcceptSerializer(accept,many=True)
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
def user_Cancel_order(request):
    order_id = request.POST['order_id']
    try:
        accept = BuyerPayment.objects.get(order=order_id)
        accept.cancel=False
        accept.save()

        serializer = BuyerPaymentSerializer(accept)
        return Response({"message": "User payment successfully.", "data": serializer.data}, status=200)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_return_order(request):
    accept_id = request.POST['accept_id']
    order_return_message = request.POST['order_return_message']
    try:
        max_accept_id = Accept.objects.aggregate(Max('id'))['id__max']
        print(max_accept_id)
        if not 1 <= int(accept_id) <= max_accept_id:
            return Response(f"Invalid accept_id. Please provide a valid ID less than or equal to {max_accept_id}.")

        unique_id = str(uuid.uuid4().int)[:9]
        order_id = "RET" + unique_id

        # buyer_user = BuyerRegistration.objects.get(user_email_id=request.session['user_email_id'])

        user = request.user
        if user.is_authenticated:
            buyer_user = BuyerRegistration.objects.get(user_email_id=user)
            accept_instance = Accept.objects.get(id=accept_id, buyer=buyer_user)
            buyer_payment_instance = BuyerPayment.objects.get(order=accept_instance.order)


            if not accept_instance=="" or buyer_payment_instance=="":
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
                return Response({"message":  " data   is empty ."}, status=200)

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
            buyer_user = BuyerRegistration.objects.get(user_email_id=user)
            member = Return.objects.filter(buyer=buyer_user)
            print(member)
            if not member=="":
                serializer = ReturnSerializer(member,many=True)
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
def user_view_product_clothe(request):
    try:
        buyer_user = Product.objects.filter(product_category="ELECTRONICS",product_sub_category="HOME AUDIO")

        if not buyer_user=="":

            serializer = ProductSerializer(buyer_user, many=True)
            return Response({"message": " user view product successfully.", "data": serializer.data}, status=200)
        else:
            return Response({"message": " product is empty ."}, status=400)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)