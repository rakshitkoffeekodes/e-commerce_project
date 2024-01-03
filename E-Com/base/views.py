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

        if user_password == user_confirm_password:
            user = User.objects.create_user(username=user_email_id, password=user_password)
            member = BuyerRegistration(user_firstname=user_firstname, user_lastname=user_lastname,
                                       user_email_id=user_email_id, user_password=user_password)
            member.save()
            user.save()
            serializer = BuyerRegistrationSerializer(member)
            return Response(serializer.data)
        else:
            return Response({"error": "password and confirm_password is not the same"}, status=400)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@api_view(['POST'])
def user_login(request):
    user_email_id = request.POST["user_email_id"]
    user_password = request.POST["user_password"]

    try:
        request.session['user_email_id'] = user_email_id
        BuyerRegistration.objects.get(user_email_id=user_email_id, user_password=user_password)
        return Response({"message": " user successfully login"}, status=200)

    except BuyerRegistration.DoesNotExist:
        return Response({"error": f"Invalid credentials {BuyerRegistration.__name__}"}, status=404)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@api_view(['POST'])
def user_profile(request):
    try:
        buyer_user = BuyerRegistration.objects.get(user_email_id=request.session['user_email_id'])
        path = request.META['HTTP_HOST']

        path1 = 'http://' + path + '/media/' + str(buyer_user.user_photo)
        buyer_user.user_photo = path1

        serializer = BuyerRegistrationSerializer(buyer_user)
        return Response({"message": " user profile successfully view.", "data": serializer.data}, status=200)

    except BuyerRegistration.DoesNotExist:
        return Response({"error": f"Error in view user profile updated: {BuyerRegistration.__name__}"}, status=404)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@api_view(['POST'])
def user_update(request):
    user_firstname = request.POST.get("user_firstname", "")
    user_lastname = request.POST.get("user_lastname", "")
    user_mobile_no = request.POST.get("user_mobile_no", "")
    user_address = request.POST.get("user_address", "")
    user_photo = request.FILES.get("user_photo")

    try:
        buyer_user = BuyerRegistration.objects.get(user_email_id=request.session['user_email_id'])
        if not user_firstname == '':
            buyer_user.user_firstname = user_firstname
        if not user_lastname == '':
            buyer_user.user_lastname = user_lastname
        if not user_mobile_no == '':
            buyer_user.user_mobile_no = user_mobile_no
        if not user_address == '':
            buyer_user.user_address = user_address
        if not user_photo == '':
            buyer_user.user_photo = user_photo
        buyer_user.save()
        serializer = BuyerRegistrationSerializer(buyer_user)
        return Response({"message": " user profile successfully updated.", "data": serializer.data}, status=200)

    except BuyerRegistration.DoesNotExist:
        return Response({"error": f"Error in  user profile updated: {BuyerRegistration.__name__}"}, status=400)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


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
    buyer_user = Product.objects.all()
    try:
        serializer = ProductSerializer(buyer_user, many=True)
        return Response({"message": " user view product successfully.", "data": serializer.data}, status=200)
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
    member = Checkout_details.objects.all()
    try:
        serializer = BuyerAddressSerializer(member, many=True)
        return Response({"message": " user  address successfully view.", "data": serializer.data}, status=200)
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

    try:
        member = Checkout_details.objects.get(address=address)
        print(member)
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


@api_view(['POST'])
def user_delete_address(request):
    address_id = request.POST["address_id"]
    try:
        member = Checkout_details.objects.get(address_id=address_id)
        member.delete()
        return Response({"message": " user profile successfully deleted."}, status=200)
    except Checkout_details.DoesNotExist:
        return Response({"error": f"Error in  user profile updated: {Checkout_details.__name__}"}, status=404)
    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@api_view(['POST'])
def user_insert_cart(request):
    qty = request.POST['qty']
    product_color = request.POST['product_color']
    product_size = request.POST['product_size']
    product = request.POST['product']
    try:
        p = Product.objects.get(id=product)
        buyer_user = BuyerRegistration.objects.get(user_email_id=request.session['user_email_id'])
        member = BuyerCart(qty=qty, product_color=product_color, product_size=product_size, total=p.product_price,
                           buyer=buyer_user, product=p)
        member.save()
        serializer = BuyerCartSerializer(member)
        return Response({"message": " user cart successfully insert .", "data": serializer.data}, status=200)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@api_view(['POST'])
def user_view_cart(request):
    member = BuyerCart.objects.all()

    try:
        serializer = BuyerCartSerializer(member, many=True)
        return Response({"message": " user cart successfully view .", "data": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@api_view(['POST'])
def user_update_cart(request):
    cart = request.POST['cart']
    qty = request.POST.get('qty')
    product_color = request.POST.get('product_color')
    product_size = request.POST.get('product_size')

    try:
        member = BuyerCart.objects.get(pk=cart)
        total = int(qty) * member.total

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
    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@api_view(['POST'])
def user_delete_cart(request):
    cart = request.POST['cart']
    print(cart)
    try:
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

        buyer_user = BuyerRegistration.objects.get(user_email_id=request.session['user_email_id'])
        p = Product.objects.get(id=product)
        c = Checkout_details.objects.get(address=Checkout)

        total = int(qty) * p.product_price
        member = BuyerPurchase(qty=qty, total=total,
                               buyer=buyer_user, product=p, checkout=c)

        member.save()
        serializer = BuyercartPurchaseSerializer(member)
        return Response({"message": " user buy Product successfully .", "data": serializer.data}, status=200)

    except Exception as e:
        return Response({"error": e.__str__()}, status=404)


@api_view(['POST'])
def user_insert_cart_buynow(request):
    cart_id = request.POST.get('cart')
    checkout_address = request.POST.get('Checkout')

    try:
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
def payment_intent(request):
    details = BuyerPurchase.objects.get(id=1)
    print(details.total)
    return Response("insert data")
    # dataDict = dict(request.data)
    # price = dataDict['price'][0]
    # product_name = dataDict['product_name'][0]
    # try:
    #   checkout_session = stripe.checkout.Session.create(
    #     line_items =[{
    #     'price_data' :{
    #       'currency' : 'usd',
    #         'product_data': {
    #           'name': product_name,
    #         },
    #       'unit_amount': price
    #     },
    #     'quantity' : 1
    #   }],
    #     mode= 'payment',
    #     # success_url= FRONTEND_CHECKOUT_SUCCESS_URL,
    #     # cancel_url= FRONTEND_CHECKOUT_FAILED_URL,
    #     )

