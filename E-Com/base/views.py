from rest_framework.response import Response
from .serlializers import *
from .models import *
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import *
from django.contrib.auth.models import User


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
            return Response("password and confirm_password is not same")

    except Exception as e:
        return Response(f"Error in data insertion: {str(e)}", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    user_email_id = request.POST["user_email_id"]
    user_password = request.POST["user_password"]

    try:
        request.session['user_email_id'] = user_email_id
        BuyerRegistration.objects.get(user_email_id=user_email_id, user_password=user_password)

        return JsonResponse({"message": "suceesfully login"})

    except BuyerRegistration.DoesNotExist:
        return JsonResponse({"message": "Invalid credentials"})

    except Exception as e:
        print(f"An error occurred: {e}")
        return JsonResponse({"message": "An error occurred"})


@api_view(['POST'])
def user_profile(request):
    try:
        buyer_user = BuyerRegistration.objects.get(user_email_id=request.session['user_email_id'])
        path = request.META['HTTP_HOST']

        path1 = 'http://' + path + '/media/' + str(buyer_user.user_photo)
        buyer_user.user_photo = path1
        data = {
            'user_photo': str(buyer_user.user_photo),
            'user_firstname': buyer_user.user_firstname,
            'user_lastname': buyer_user.user_lastname,
            'user_email_id': buyer_user.user_email_id,
            'user_mobile_no': buyer_user.user_mobile_no,
            'user_address': buyer_user.user_address
        }
        return JsonResponse({'Profile': data})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def user_update(request):
    user_firstname = request.POST.get("user_firstname")
    user_lastname = request.POST.get("user_lastname")
    user_email_id = request.POST.get("user_email_id")
    user_mobile_no = request.POST.get("user_mobile_no")
    user_address = request.POST.get("user_address")
    user_photo = request.FILES["user_photo"]

    try:
        buyer_user = BuyerRegistration.objects.get(user_email_id=request.session['user_email_id'])
        path = request.META['HTTP_HOST']
        path1 = 'http://' + path + '/media/media/' + str(user_photo)
        print(path1)
        user_photo = path1
        member = BuyerRegistration(user_firstname=user_firstname, user_lastname=user_lastname,
                                   user_email_id=user_email_id, user_mobile_no=user_mobile_no,
                                   user_address=user_address, user_photo=user_photo)
        member.save()
        data = {
            'user_photo': str(user_photo),
            'user_firstname': user_firstname,
            'user_lastname': user_lastname,
            'user_email_id': user_email_id,
            'user_mobile_no': user_mobile_no,
            'user_address': user_address
        }
        return JsonResponse({'Profile': data})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def user_search_product(request):
    search = request.POST.get("search")

    try:
        member = BuyerRegistration.objects.filter(user_firstname__istartswith=search)
        print(member.values())
        serializer = BuyerRegistrationSerializer(member, many=True)
        return Response(serializer.data)
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def user_view_product(request):
    buyer_user = BuyerRegistration.objects.all()
    print(buyer_user)

    try:
        serializer = BuyerRegistrationSerializer(buyer_user, many=True)
        return Response(serializer.data)
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


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
        return Response(serializer.data)
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def user_view_address(request):
    member = Checkout_details.objects.all()

    try:
        serializer = BuyerAddressSerializer(member, many=True)
        return Response(serializer.data)
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def user_update_address(request):
    address_id = request.POST["address_id"]
    street_address = request.POST.get("street_address")
    apartment_address = request.POST.get("apartment_address")
    pincode = request.POST.get("pincode")
    city = request.POST.get("city")
    select_state = request.POST.get("select_state")
    ord_rec_name = request.POST.get("ord_rec_name")
    ord_rec_mobile_no = request.POST.get("ord_rec_mobile_no")

    try:
        member = Checkout_details.objects.get(address_id=address_id)
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
        return Response(serializer.data)
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def user_delete_address(request):
    address_id = request.POST["address_id"]
    try:
        member = Checkout_details.objects.get(address_id=address_id)
        member.delete()
        return JsonResponse(
            {'success': 'str(id) + "Record has been successfully deleted"', 'status': status.HTTP_200_OK})

    except Checkout_details.DoesNotExist:
        return JsonResponse({"message": "Invalid enter id By user "})


@api_view(['POST'])
def user_insert_cart(request):
    qty = request.POST['qty']
    total = request.POST['total']
    product_size = request.POST['product_size']
    try:
        buyer_user = BuyerRegistration.objects.get(user_email_id=request.session['user_email_id'])


    except Exception as e:
        return JsonResponse({'Message': e.__str__()})

