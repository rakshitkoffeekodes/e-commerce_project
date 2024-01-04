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
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
@api_view(['POST'])
def user_registration(request):
    user_firstname = request.POST["user_firstname"]
    user_lastname = request.POST["user_lastname"]
    user_email_id = request.POST["user_email_id"]
    user_password = request.POST["user_password"]
    user_confirm_password = request.POST["user_confirm_password"]

    try:
        if BuyerRegistration.objects.filter(user_email_id=user_email_id).exists():
            return Response({"error": "Email is already registered"}, status=400)

        if user_password == user_confirm_password:
            user = User.objects.create_user(username=user_email_id, password=user_password)
            member = BuyerRegistration(user_firstname=user_firstname, user_lastname=user_lastname,
                                       user_email_id=user_email_id, user_password=user_password)
            user.save()
            member.save()
            serializer = BuyerRegistrationSerializer(member)
            return Response(serializer.data)
        else:
            return Response({"error": "Password and confirm_password do not match"}, status=400)

    except Exception as e:
        return Response({"error": str(e)}, status=404)

@api_view(['POST'])
def user_login(request):
    user_email_id = request.POST["user_email_id"]
    user_password = request.POST["user_password"]

    try:
        request.session['user_email_id'] = user_email_id
        member=BuyerRegistration.objects.get(user_email_id=user_email_id)
        if member.user_password ==user_password:
            return Response({"message": " user successfully login"}, status=200)
        else:
            return Response({"message": " Invalid password"}, status=200)

    except BuyerRegistration.DoesNotExist:
        return Response({"error": f"Invalid credentials {BuyerRegistration.__name__}"}, status=404)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@api_view(['POST'])
def user_profile(request):

    try:
        buyer_user = BuyerRegistration.objects.get(user_email_id=request.session['user_email_id'])

        if buyer_user!="":
            path = request.META['HTTP_HOST']

            path1 = 'http://' + path + '/media/' + str(buyer_user.user_photo)
            buyer_user.user_photo = path1

            serializer = BuyerRegistrationSerializer(buyer_user)
            return Response({"message": " user profile successfully view.", "data": serializer.data}, status=200)
        else:
            return Response({"message": " user is not active"}, status=400)


    except BuyerRegistration.DoesNotExist:
        return Response({"error": f"Error in view user profile : {BuyerRegistration.__name__}"}, status=404)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


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

        buyer_user = BuyerRegistration.objects.get(user_email_id=request.session['user_email_id'])

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

    except BuyerRegistration.DoesNotExist:
        return Response({"error": f"Error in user profile update: {BuyerRegistration.__name__}"}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

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


        member = Checkout_details(street_address=street_address, apartment_address=apartment_address,
                                  pincode=pincode, city=city, ord_rec_mobile_no=ord_rec_mobile_no,
                                  select_state=select_state, ord_rec_name=ord_rec_name)
        member.save()
        serializer = BuyerAddressSerializer(member)
        return Response({"message": " user  address successfully insert.", "data": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@api_view(['POST'])
def user_view_address(request):
    try:
        member = Checkout_details.objects.all()
        if member !="":
            serializer = BuyerAddressSerializer(member, many=True)
            return Response({"message": " user  address successfully view.", "data": serializer.data}, status=200)
        else:
            return Response({"message": " address is empty ."}, status=400)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


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
    print(len(address))

    try:
        member = Checkout_details.objects.all()
        if (len(address) == 0) or len(address)>=len(member) :
            return Response({"error": "Invalid address id. Please select valid address id."}, status=400)

        if not (pincode.isdigit() and len(pincode) == 6):
            return Response({"error": "Invalid pincode number. Please provide a 6-digit number."}, status=400)

        if not (ord_rec_mobile_no.isdigit() and len(ord_rec_mobile_no) == 10):
            return Response({"error": "Invalid mobile number. Please provide a 10-digit number."}, status=400)

        member = Checkout_details.objects.get(address=address)
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

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)

    except Checkout_details.DoesNotExist:
        return Response({"error": f"Error in address profile update: {Checkout_details.__name__}"}, status=404)



@api_view(['POST'])
def user_delete_address(request):
    address_id = request.POST["address_id"]
    print(type(address_id))
    try:
        member = Checkout_details.objects.all()
        if (len(address_id) == 0) or len(address_id) >= len(member) :
            return Response({"error": "Invalid address id. Please select valid address id."}, status=400)

        member = Checkout_details.objects.get(address_id=address_id)
        member.delete()
        return Response({"message": " user profile successfully deleted."}, status=200)
    except Checkout_details.DoesNotExist:
        return Response({"error": f"Error in  user profile updated: {Checkout_details.__name__}"}, status=404)
    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@api_view(['POST'])
def user_insert_cart(request):
    product_color = request.POST['product_color']
    product_size = request.POST['product_size']
    product = request.POST['product']
    try:
        product_value = Product.objects.get(id=product)
        if not product_value=="":
            return Response({"error": "Product is empty ."}, status=400)

        buyer_user = BuyerRegistration.objects.get(user_email_id=request.session['user_email_id'])
        member = BuyerCart(qty=1, product_color=product_color, product_size=product_size, total=product_value.product_price,
                           buyer=buyer_user, product=product_value)
        member.save()
        serializer = BuyerCartSerializer(member)
        return Response({"message": " user cart successfully insert .", "data": serializer.data}, status=200)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)

    except Product.DoesNotExist:
        return Response({"error": f"Error in  cart  insert: {Product.__name__}"}, status=404)


@api_view(['POST'])
def user_view_cart(request):


    try:
        member = BuyerCart.objects.all()
        if member != "":
            serializer = BuyerCartSerializer(member, many=True)
            return Response({"message": " user cart successfully view .", "data": serializer.data}, status=200)
        else:
            return Response({"message": " address is empty ."}, status=400)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@api_view(['POST'])
def user_update_cart(request):
    cart = request.POST['cart']
    qty = request.POST.get('qty')
    product_color = request.POST.get('product_color')
    product_size = request.POST.get('product_size')

    try:

        member = Checkout_details.objects.all()
        if not 1 <= int(qty) <= 100 and (qty.isdigit()):
            return Response({"message": "Invalid qty number. Qty should be between 1 and 100."}, status=400)

        if (len(cart) == 0) or (len(cart)<=len(member)) :
            return Response({"error": "Invalid cart id. Please select valid cart id."}, status=400)

        member = BuyerCart.objects.get(pk=cart)
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
    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@api_view(['POST'])
def user_delete_cart(request):
    cart = request.POST['cart']
    try:
        member = Checkout_details.objects.all()
        if (len(cart) == 0) or (len(cart)<=len(member)):
            return Response({"error": "Invalid cart id. Please select valid cart id."}, status=400)

        member = BuyerCart.objects.get(id=cart)
        member.delete()
        return Response({"message": " user cart successfully deleted."}, status=200)

    except Checkout_details.DoesNotExist:
        return Response({"error": f"user Invalid id select {Checkout_details.__name__}"}, status=404)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@api_view(['POST'])
def user_insert_buynow(request):
    qty = request.POST['qty']
    product = request.POST['product']
    Checkout = request.POST['Checkout']
    try:
        product_value = Product.objects.all()
        chekout_value = Checkout_details.objects.all()

        if not 1 <= int(qty) <= 100 and (qty.isdigit()):
            return Response({"message": "Invalid qty number. Qty should be between 1 and 100."}, status=400)

        if (len(product) == 0) or len(product)>=len(product_value) :
            return Response({"error": "Invalid product id. Please select valid product id."}, status=400)

        if (len(Checkout) == 0) or len(Checkout)>=len(chekout_value) :
            return Response({"error": "Invalid chekout id. Please select valid chekout id."}, status=400)


        buyer_user = BuyerRegistration.objects.get(user_email_id=request.session['user_email_id'])
        product_data = Product.objects.get(id=product)
        checkout_data = Checkout_details.objects.get(address=Checkout)
        total = int(qty) * product_data.product_price

        if not product_data=="" and checkout_data=="":
            member = BuyerPurchase(qty=qty, total=total,
                                   buyer=buyer_user, product=product_data, checkout=checkout_data)

            member.save()
            serializer = BuyercartPurchaseSerializer(member)
            return Response({"message": " user buy Product successfully .", "data": serializer.data}, status=200)
        else:
            return Response({"message": " product is empty ."}, status=400)


    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@api_view(['POST'])
def user_insert_cart_buynow(request):
    cart_id = request.POST.get('cart')
    checkout_address = request.POST.get('Checkout')

    try:
        cart_value = BuyerCart.objects.all()
        checkout_value = Checkout_details.objects.all()

        # Validate cart_id
        if not cart_id or not cart_id.isdigit() or int(cart_id) < 1:
            return Response({"error": "Invalid cart id. Please select a valid cart id."}, status=400)

        # Validate checkout_address
        if not checkout_address or len(checkout_address) >= len(checkout_value):
            return Response({"error": "Invalid checkout address. Please select a valid checkout address."}, status=400)

        buyer_user = BuyerRegistration.objects.get(user_email_id=request.session['user_email_id'])
        cart = BuyerCart.objects.get(id=cart_id)
        checkout = Checkout_details.objects.get(address=checkout_address)

        member = BuyerPurchase(
            qty=cart.qty, total=cart.total, buyer=buyer_user,
            product=cart.product, cart=cart, checkout=checkout
        )
        member.save()
        print(member.cart, member.product)
        serializer = BuyercartPurchaseSerializer(member)
        return Response({"message": " user cart to buy  Product successfully .", "data": serializer.data}, status=200)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


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


@api_view(['POST'])
def user_insert_feedback(request):
    feedback_description = request.POST['feedback_description']
    feedback_rating = request.POST['feedback_rating']
    feedback_photo = request.FILES['feedback_photo']
    feedback_product = request.POST['feedback_product']
    try:

        buyer_user = BuyerRegistration.objects.get(user_email_id=request.session['user_email_id'])
        p = Product.objects.get(id=feedback_product)
        member = BuyerFeedback(
            feedback_description=feedback_description,
            feedback_rating=feedback_rating,
            feedback_photo=feedback_photo,
            feedback_product=p,
            feedback_login=buyer_user,
        )
        print(member)
        member.save()
        serializer = BuyerFeedbackSerializer(member)
        return Response({"message": " user feedback successfully insert .", "data": serializer.data}, status=200)


    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@api_view(['POST'])
def user_view_feedback(request):
    member = BuyerFeedback.objects.all()

    try:
        serializer = BuyerFeedbackSerializer(member, many=True)
        return Response({"message": " user feedback successfully view .", "data": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


stripe.api_key = 'sk_test_51OU5FMSAvmPjZJjlUaHxMRIUgI3enoGyrOyvGh1LP5OOl7UuUDZxkJemUPCCi6hWVZ2yWyxU7ADIe7tsN5wVdHVN00D0dS4gP0'


@csrf_exempt
@api_view(['POST'])
def create_payment_intent(request):
    p = request.POST.get('p')
    try:
        unique_id = str(uuid.uuid4().int)[:12]
        order_id = "ORD" + unique_id
        print(order_id)
        buyer_user = BuyerRegistration.objects.get(user_email_id=request.session['user_email_id'])
        details=BuyerPurchase.objects.get(id=p)
        amount = int(request.POST.get('amount'))
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='inr',
        )

        payment = BuyerPayment.objects.create(
            amount=amount,
            currency='INR',
            status='Success',
            payment_intent_id=intent.id,
            details=details,
            buyer=buyer_user,
            order=order_id

        )
        serializer = BuyerPaymentSerializer(payment)
        return Response({"message": " user payment successfully .", "data": serializer.data}, status=200)


    except Exception as e:
        return Response({"error": e.__str__()}, status=404)

@api_view(['POST'])
def stripe_config(request):
    stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
    return Response(stripe_config)

@csrf_exempt
@api_view(['POST'])
def payment_intent(request):
    domain_url = 'http://127.0.0.1:8000'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    success_url = 'https://example.com/success/'
    cancel_url = 'https://example.com/cancel/'
    # try:
    # checkout_session = stripe.checkout.Session.create(
    #     success_url=domain_url + success_url,
    #     cancel_url=domain_url + cancel_url,
    #     payment_method_types=['card'],
    #     mode='payment',
    #     line_items=[
    #         {
    #             'name': 'T-shirt',
    #             'quantity': 1,
    #             'currency': 'usd',
    #             'amount': '2000',
    #         }
    #     ]
    # )
    checkout_session = stripe.checkout.Session.create(
        success_url=domain_url + success_url,
        cancel_url=domain_url + cancel_url,
        payment_method_types=['card'],
        mode='payment',
        line_items=[
            {
                'name': 'T-shirt',
                'quantity': 1,
                'currency': 'usd',
                'amount': '2000',
            }
        ]
    )
    print("Checkout Session:", checkout_session)
    return Response({'sessionId': checkout_session['id']})
    # return Response({'sessionId': checkout_session['id']})
    # except Exception as e:
    #     return Response({'error': str(e)})

# def payment_intent(request):
#     # ... (existing code)
#
#
#
#     print(f"Success URL: {success_url}")
#     print(f"Cancel URL: {cancel_url}")
#
#     checkout_session = stripe.checkout.Session.create(
#         success_url=success_url,
#         cancel_url=cancel_url,
#         # other parameters...
#     )
#     # ... (remaining code)