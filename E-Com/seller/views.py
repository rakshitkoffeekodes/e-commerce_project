import os
import datetime
import random
# from fpdf import FPDF
import qrcode
from base.models import *
from django.conf import settings
from django.core.files.storage import default_storage
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password
from .serilizers import *


# Create your views here.


@api_view(['POST'])
def register(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    conform_password = request.POST['confirm_password']
    try:
        if password == conform_password:
            Register.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=make_password(password)
            )
            return JsonResponse({'Message': f'Register Success {first_name}'})
        else:
            return JsonResponse({'Message': 'Password Not Match.'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def login(request):
    email = request.POST['email']
    password = request.POST['password']

    try:
        seller_user = Register.objects.get(email=email)
        if check_password(password, seller_user.password):
            request.session['email'] = email
            return JsonResponse({'Message': f'{seller_user.first_name} Login Successfully.'})
        else:
            return JsonResponse({'Message': 'Password Not Match'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['GET'])
def logout(request):
    del request.session['email']
    return JsonResponse({'Message': 'Logout Successfully.'})


@api_view(['GET'])
def profile(request):
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        path = request.META['HTTP_HOST']
        path1 = 'http://' + path + '/media/' + str(seller_user.profile_picture)
        seller_user.profile_picture = path1
        data = {
            'Profile Image': str(seller_user.profile_picture),
            'First Name': seller_user.first_name,
            'Last Name': seller_user.last_name,
            'Email': seller_user.email,
            'Mobile Number': seller_user.mobile_no,
            'Address': seller_user.address
        }
        return JsonResponse({'Profile': data})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def update_profile(request):
    profile_picture = request.FILES.get('profile_image', '')
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    email = request.POST.get('email', '')
    mobile_no = request.POST.get('mobile_no', '')
    address = request.POST.get('address', '')

    try:
        seller_user = Register.objects.get(email=request.session['email'])
        if not profile_picture == '':
            seller_user.profile_picture = profile_picture
        if not first_name == '':
            seller_user.first_name = first_name
        if not last_name == '':
            seller_user.last_name = last_name
        if not email == '':
            seller_user.email = email
        if not mobile_no == '':
            seller_user.mobile_no = mobile_no
        if not address == '':
            seller_user.address = address
        seller_user.save()
        return JsonResponse({'Message': 'Profile Update Successfully.'})

    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def add_product(request):
    product_category = request.POST['product_category']
    product_items = request.POST['product_items']
    product_images = request.FILES.getlist('product_images')
    SKU = request.POST['SKU']
    product_name = request.POST['product_name']
    product_price = request.POST['product_price']
    product_sale_price = request.POST['product_sale_price']
    product_quantity = request.POST['product_quantity']
    product_branding = request.POST['product_branding']
    product_tags = request.POST['product_tags']
    product_size = request.POST['product_size']
    product_color = request.POST['product_color']
    product_fabric = request.POST['product_fabric']
    product_description = request.POST['product_description']

    try:
        seller_user = Register.objects.get(email=request.session['email'])
        product_add = Product()
        product_add.product_category = product_category.upper()
        product_add.product_items = product_items.upper()
        product_add.product_images = [
            default_storage.save(os.path.join(settings.MEDIA_ROOT, 'Product', image.name.replace(' ', '_')), image)
            for image in product_images]
        print(product_add.product_images)
        product_add.SKU = SKU
        product_add.product_name = product_name
        product_add.product_price = product_price
        product_add.product_sale_price = product_sale_price
        product_add.product_quantity = product_quantity
        product_add.product_branding = product_branding
        product_add.product_tags = product_tags
        product_add.product_size = product_size
        product_add.product_color = product_color
        product_add.product_fabric = product_fabric
        product_add.product_description = product_description
        product_add.product_date = datetime.datetime.now()
        product_add.product_seller = seller_user
        product_add.save()
        return JsonResponse({'message': 'Product Add Successfully.'})

    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['GET'])
def view_all_product(request):
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        all_product = Product.objects.filter(product_seller=seller_user)
        all_product_list = []
        for i in all_product:
            path = request.META['HTTP_HOST']
            path1 = ['http://' + path + '/media/' + i for i in i.product_images]
            i.product_images = path1
            products = {
                'product_images': i.product_images,
                'SKU': i.SKU,
                'product_name': i.product_name,
                'product_price': i.product_price,
                'product_sale_price': i.product_sale_price,
                'product_quantity': i.product_quantity,
                'product_category': i.product_category,
                'product_items': i.product_items,
                'product_branding': i.product_branding,
                'product_tags': i.product_tags,
                'product_size': i.product_size,
                'product_color': i.product_color,
                'product_fabric': i.product_fabric,
                'product_description': i.product_description,
            }
            all_product_list.append(products)
        return JsonResponse({'Products': all_product_list})

    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def update_product(request):
    primary_key = request.POST['primary_key']
    product_category = request.POST.get('product_category')
    product_items = request.POST.get('product_items')
    product_images = request.FILES.getlist('product_images')
    SKU = request.POST.get('SKU')
    product_name = request.POST.get('product_name')
    product_price = request.POST.get('product_price')
    product_sale_price = request.POST.get('product_sale_price')
    product_quantity = request.POST.get('product_quantity')
    product_branding = request.POST.get('product_branding')
    product_tags = request.POST.get('product_tags')
    product_size = request.POST.get('product_size')
    product_color = request.POST.get('product_color')
    product_fabric = request.POST.get('product_fabric')
    product_description = request.POST.get('product_description')
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        update = Product.objects.get(product_seller=seller_user, id=primary_key)
        if len(product_images) != 0:
            if not product_category == '':
                update.product_category = product_category
            if not product_items == '':
                update.product_items = product_items
            if not product_images == '':
                update.product_images = [
                    default_storage.save(os.path.join(settings.MEDIA_ROOT, 'Product', image.name.replace(' ', '_')),
                                         image) for image in product_images]
            if not SKU == '':
                update.SKU = SKU
            if not product_name == '':
                update.product_name = product_name
            if not product_price == '':
                update.product_price = product_price
            if not product_sale_price == '':
                update.product_sale_price = product_sale_price
            if not product_quantity == '':
                update.product_quantity = product_quantity
            if not product_branding == '':
                update.product_branding = product_branding
            if not product_tags == '':
                update.product_tags = product_tags
            if not product_size == '':
                update.product_size = product_size
            if not product_color == '':
                update.product_color = product_color
            if not product_fabric == '':
                update.product_fabric = product_fabric
            if not product_description == '':
                update.product_description = product_description
        else:
            if not product_category == '':
                update.product_category = product_category
            if not product_items == '':
                update.product_items = product_items
            if not SKU == '':
                update.SKU = SKU
            if not product_name == '':
                update.product_name = product_name
            if not product_price == '':
                update.product_price = product_price
            if not product_sale_price == '':
                update.product_sale_price = product_sale_price
            if not product_quantity == '':
                update.product_quantity = product_quantity
            if not product_branding == '':
                update.product_branding = product_branding
            if not product_tags == '':
                update.product_tags = product_tags
            if not product_size == '':
                update.product_size = product_size
            if not product_color == '':
                update.product_color = product_color
            if not product_fabric == '':
                update.product_fabric = product_fabric
            if not product_description == '':
                update.product_description = product_description
        update.save()
        return JsonResponse({'Message': 'Update Product Successfully.'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def delete_product(request):
    primary_key = request.POST['primary_key']
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        delete = Product.objects.get(product_seller=seller_user, id=primary_key)
        delete.delete()
        return JsonResponse({'Message': 'Delete Product Successfully.'})

    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['GET'])
def pending_order(request):
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        buyer_order = Payment.objects.filter(details__cart__status=True)
        buyer_all_order = Order.objects.filter(details__cart__product__product_seller=seller_user,
                                               details__status=True).only(
            'order')
        list2 = [i.order for i in buyer_all_order]
        for i in buyer_order:
            if i.order not in list2:
                c_id = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H"]
                id2 = random.choices(c_id, k=9)
                company = "".join(id2)
                orders = Order()
                orders.details = i.details
                orders.product = i.details.cart.product
                orders.buyer = i.details.cart.buyer
                orders.qty = i.details.cart.qty
                orders.product_color = i.details.cart.product_color
                orders.product_size = i.details.cart.product_size
                orders.total = i.details.cart.total
                orders.order = i.order
                orders.company = company
                orders.order_date = datetime.datetime.now()
                orders.dispatch_date = orders.order_date + datetime.timedelta(days=4)
                orders.save()
        view_all_order = Order.objects.filter(details__cart__product__product_seller=seller_user, status=True)
        all_order = []
        for i in view_all_order:
            path = request.META['HTTP_HOST']
            path1 = ['http://' + path + '/media/' + i for i in i.details.cart.product.product_images]
            i.details.cart.product.product_images = path1
            data = {
                'Order ID': i.order,
                'Image': i.details.cart.product.product_images,
                'Name': i.details.cart.product.product_name,
                'SKU ID': i.details.cart.product.SKU,
                'Company ID': i.company,
                'Quantity': i.details.cart.qty,
                'Size': i.details.cart.product.product_size,
                'Dispatch Date/ SLA': i.dispatch_date
            }
            all_order.append(data)
        return JsonResponse({'View All Order': all_order})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def filter_order_date(request):
    start_time = datetime.time(00, 00, 00)
    end_time = datetime.time(23, 59, 59)
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    try:
        filter_data_list = []
        seller_user = Register.objects.get(email=request.session['email'])
        start_object = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        start_datetime = datetime.datetime(year=start_object.year, month=start_object.month, day=start_object.day,
                                           hour=start_time.hour, minute=start_time.minute, second=start_time.second)
        end_object = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_datetime = datetime.datetime(year=end_object.year, month=end_object.month, day=end_object.day,
                                         hour=end_time.hour, minute=end_time.minute, second=end_time.second)
        filter_data = Order.objects.filter(order_date__range=(start_datetime, end_datetime),
                                           details__cart__product__product_seller=seller_user,
                                           details__cart__status=True, status=True)
        for i in filter_data:
            path = request.META['HTTP_HOST']
            path1 = ['http://' + path + '/media/' + i for i in i.details.cart.product.product_images]
            i.details.cart.product.product_images = path1
            dispatch_date = i.dispatch_date
            dispatch_day = dispatch_date.day
            dispatch_month = dispatch_date.strftime('%B')
            data = {
                'Order ID': i.order,
                'Image': i.details.cart.product.product_images,
                'Name': i.details.cart.product.product_name,
                'SKU ID': i.details.cart.product.SKU,
                'Company ID': i.company,
                'Quantity': i.details.cart.qty,
                'Size': i.details.cart.product.product_size,
                'Dispatch Date/ SLA': f'{dispatch_day} {dispatch_month}'
            }
            filter_data_list.append(data)
        return JsonResponse({'Filter Order': filter_data_list})

    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def filter_dispatch_date(request):
    start_time = datetime.time(00, 00, 00)
    end_time = datetime.time(23, 59, 59)
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    try:
        filter_data_list = []
        seller_user = Register.objects.get(email=request.session['email'])
        start_object = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        start_datetime = datetime.datetime(year=start_object.year, month=start_object.month, day=start_object.day,
                                           hour=start_time.hour, minute=start_time.minute, second=start_time.second)
        end_object = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_datetime = datetime.datetime(year=end_object.year, month=end_object.month, day=end_object.day,
                                         hour=end_time.hour, minute=end_time.minute, second=end_time.second)
        filter_data = Order.objects.filter(dispatch_date__range=(start_datetime, end_datetime),
                                           details__cart__product__product_seller=seller_user,
                                           details__cart__status=True, status=True)
        for i in filter_data:
            path = request.META['HTTP_HOST']
            path1 = ['http://' + path + '/media/' + i for i in i.details.cart.product.product_images]
            i.details.cart.product.product_images = path1
            dispatch_date = i.dispatch_date
            dispatch_day = dispatch_date.day
            dispatch_month = dispatch_date.strftime('%B')
            data = {
                'Order ID': i.order,
                'Image': i.details.cart.product.product_images,
                'Name': i.details.cart.product.product_name,
                'SKU ID': i.details.cart.product.SKU,
                'Company ID': i.company,
                'Quantity': i.details.cart.qty,
                'Size': i.details.cart.product.product_size,
                'Dispatch Date/ SLA': f'{dispatch_day} {dispatch_month}'
            }
            filter_data_list.append(data)
        return JsonResponse({'Filter Order': filter_data_list})

    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def order_search(request):
    search = request.POST.get('search', '')
    search_data = []
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        search_order = Order.objects.filter(
            Q(order__icontains=search) | Q(company__icontains=search) | Q(
                details__cart__product__SKU__icontains=search),
            details__cart__product__product_seller=seller_user, status=True)
        if search_order.count() != 0 and search != '':
            for i in search_order:
                path = request.META['HTTP_HOST']
                path1 = ['http://' + path + '/media/' + i for i in i.details.cart.product.product_images]
                i.details.cart.product.product_images = path1
                dispatch_date = i.dispatch_date
                dispatch_day = dispatch_date.day
                dispatch_month = dispatch_date.strftime('%B')
                data = {
                    'Order ID': i.order,
                    'Image': i.details.cart.product.product_images,
                    'Name': i.details.cart.product.product_name,
                    'SKU ID': i.details.cart.product.SKU,
                    'Company ID': i.company,
                    'Quantity': i.details.cart.qty,
                    'Size': i.details.cart.product.product_size,
                    'Dispatch Date/ SLA': f'{dispatch_day} {dispatch_month}'
                }
                search_data.append(data)
            return JsonResponse({'Message': search_data})
        else:
            return JsonResponse({'Message': 'Product Is Not Found'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def order_accept(request):
    primary_key = request.POST['primary_key']
    id_list = primary_key.split(',')
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        if not len(id_list) > 1:
            accept = Order.objects.get(id=primary_key, status=True, details__cart__product__product_seller=seller_user)
            accept_order = Accept()
            accept_order.order = accept
            accept_order.product = accept.product
            accept_order.buyer = accept.buyer
            accept_order.qty = accept.qty
            accept_order.product_color = accept.product_color
            accept_order.product_size = accept.product_size
            accept_order.total = accept.total
            accept_order.save()
            accept.status = False
            accept.save()
            product = Product.objects.get(id=accept.product.id)
            product.product_quantity = product.product_quantity - accept.qty
            product.save()
            return JsonResponse({'Message': 'Order Accept'})
        else:
            for i in id_list:
                accept = Order.objects.get(id=i, status=True, details__cart__product__product_seller=seller_user)
                print(accept)
                accept_order = Accept()
                accept_order.order = accept
                accept_order.product = accept.product
                accept_order.buyer = accept.buyer
                accept_order.qty = accept.qty
                accept_order.product_color = accept.product_color
                accept_order.product_size = accept.product_size
                accept_order.total = accept.total
                accept_order.save()
                accept.status = False
                accept.save()
                product = Product.objects.get(id=accept.product.id)
                product.product_quantity = product.product_quantity - accept.qty
                product.save()
            return JsonResponse({'Message': 'Order Accept'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['GET'])
def ready_to_ship(request):
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        view_accept_all_order = Accept.objects.filter(status=True, order__product__product_seller=seller_user)
        accept_orders = []
        for i in view_accept_all_order:
            path = request.META['HTTP_HOST']
            path1 = ['http://' + path + '/media/' + i for i in i.product.product_images]
            i.product.product_images = path1
            dispatch_date = i.order.dispatch_date
            dispatch_day = dispatch_date.day
            dispatch_month = dispatch_date.strftime('%B')
            data = {
                'Order ID': i.order.order,
                'Image': i.product.product_images,
                'Name': i.product.product_name,
                'SKU ID': i.product.SKU,
                'Company ID': i.order.company,
                'Quantity': i.qty,
                'Size': i.product.product_size,
                'Dispatch Date/ SLA': f'{dispatch_day} {dispatch_month}'
            }
            accept_orders.append(data)

        return JsonResponse({'Message': accept_orders})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


def label_data(path2, label, seller_user, purchase_order_no, invoice_no, invoice_date, total, tax):
    # pdf = FPDF()
    # pdf.add_page()
    # # set font style and size for pdf
    # pdf.set_font('Arial', size=16)
    # pdf.cell(200, 10, txt="'QR Code': {{path2}}", ln=2, align='C')
    # pdf.output('Attempt.pdf')
    data = {
        'QR Code': path2,
        'Customer Name': label.buyer.user_firstname + ' ' + label.buyer.user_lastname,
        'Customer Address': label.buyer.user_address,
        'Seller Name': seller_user.first_name + seller_user.last_name,
        'Seller Address': seller_user.address,
        'Product Details': {'SKU': label.product.SKU, 'Size': label.product.product_size, 'Qty': label.qty,
                            'Color': label.product_color, 'Order No.': label.order.order},
        'Tax Invoice': {'Ship To': (
            label.order.details.ord_rec_name, label.order.details.street_address,
            label.order.details.apartment_address, label.order.details.pincode),
            'Sold By': (seller_user.first_name + seller_user.last_name, seller_user.address),
            'Purchase Order No.': purchase_order_no, 'Invoice No.': invoice_no, 'Order Date': label.order.order_date,
            'Invoice Date': invoice_date},
        'Description': label.product.product_name, 'Qty': label.qty, 'Gross Amount': total,
        'Taxable Value': label.total, 'Taxes': f'GST RS.{tax}', 'Total': total
    }
    return data


@api_view(['POST'])
def shipping_label(request):
    primary_key = request.POST['primary_key']
    key_list = primary_key.split(',')
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        purchase = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        invoice = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        purchase_order = random.choices(purchase, k=12)
        purchase_order_no = "".join(purchase_order)
        invoice_1 = random.choices(purchase + invoice, k=11)
        invoice_no = "".join(invoice_1)
        invoice_date = datetime.date.today()
        tax, gst1, gst2, gst3 = 0, 5.0, 12.0, 18.0
        if len(key_list) == 1:
            label = Accept.objects.get(id=primary_key, status=True, order__product__product_seller=seller_user)
            if label.order.product.product_category in ['BOOKS', 'BEAUTY', 'FURNITURE', 'GARDEN']:
                tax = label.total * gst1 / 100
            elif label.order.product.product_category in ['CLOTHE', 'MEN ACCESSORIES', 'WOMEN ACCESSORIES']:
                tax = label.total * gst2 / 100
            elif label.order.product.product_category == 'ELECTRONICS':
                tax = label.total * gst3 / 100
            total = tax + label.total
            path = 'D:\Task\E-Com\media\code'
            image = qrcode.make(label.order.order)
            name = "bcode.png"
            image.save(os.path.join(path, name))
            path1 = request.META['HTTP_HOST']
            path2 = ['http://' + path1 + '/media/code/bcode.png']
            data = label_data(path2, label, seller_user, purchase_order_no, invoice_no, invoice_date, total, tax)
            return JsonResponse({'Label Data': data})

        else:
            data_list = []
            for i in key_list:
                label = Accept.objects.get(id=i, status=True, order__product__product_seller=seller_user)
                if label.order.product.product_category in ['BOOKS', 'BEAUTY', 'FURNITURE', 'GARDEN']:
                    tax = label.total * gst1 / 100
                elif label.order.product.product_category in ['CLOTHE', 'MEN ACCESSORIES', 'WOMEN ACCESSORIES']:
                    tax = label.total * gst2 / 100
                elif label.order.product.product_category == 'ELECTRONICS':
                    tax = label.total * gst3 / 100
                total = tax + label.total
                path = 'D:\Task\E-Com\media\code'
                image = qrcode.make(label.order.order)
                name = "bcode.png"
                image.save(os.path.join(path, name))
                path1 = request.META['HTTP_HOST']
                path2 = ['http://' + path1 + '/media/code/bcode.png']
                data = label_data(path2, label, seller_user, purchase_order_no, invoice_no, invoice_date, total, tax)
                data_list.append(data)
            return JsonResponse({'Label Data': data_list})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def cancel_order(request):
    primary_key = request.POST['primary_key']
    id_list = primary_key.split(',')
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        if not len(id_list) > 1:
            cancel = Order.objects.get(id=primary_key, status=True, details__cart__product__product_seller=seller_user)
            order_cancel = Cancel()
            order_cancel.order = cancel
            order_cancel.product = cancel.product
            order_cancel.buyer = cancel.buyer
            order_cancel.qty = cancel.qty
            order_cancel.product_color = cancel.product_color
            order_cancel.product_size = cancel.product_size
            order_cancel.total = cancel.total
            order_cancel.save()
            cancel.status = False
            cancel.save()
            product = Product.objects.get(id=cancel.product.id)
            product.product_quantity = product.product_quantity + cancel.qty
            product.save()
            return JsonResponse({'Message': 'Order Cancel'})
        else:
            for i in id_list:
                cancel = Order.objects.get(id=i, status=True, details__cart__product__product_seller=seller_user)
                order_cancel = Cancel()
                order_cancel.order = cancel
                order_cancel.product = cancel.product
                order_cancel.buyer = cancel.buyer
                order_cancel.qty = cancel.qty
                order_cancel.product_color = cancel.product_color
                order_cancel.product_size = cancel.product_size
                order_cancel.total = cancel.total
                order_cancel.save()
                product = Product.objects.get(id=cancel.product.id)
                product.product_quantity = product.product_quantity + cancel.qty
                product.save()
                cancel.status = False
                cancel.save()
            return JsonResponse({'Message': 'Order Cancel'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['GET'])
def cancelled(request):
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        view_cancel_all_order = Cancel.objects.filter(status=True, order__product__product_seller=seller_user)
        cancel_orders = []
        for i in view_cancel_all_order:
            path = request.META['HTTP_HOST']
            path1 = ['http://' + path + '/media/' + i for i in i.product.product_images]
            i.product.product_images = path1
            data = {
                'Image': i.product.product_images,
                'Name': i.product.product_name,
                'Order ID': i.order.order,
                'SKU ID': i.product.SKU,
                'Company ID': i.order.company,
                'Quantity': i.qty,
                'Size': i.product.product_size,
            }
            cancel_orders.append(data)

        return JsonResponse({'Message': cancel_orders})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['GET'])
def pricing(request):
    seller_user = Register.objects.get(email=request.session['email'])
    product = Product.objects.filter(product_seller=seller_user)
    all_product = []
    for i in product:
        order = Order.objects.filter(product=i, product__product_seller=seller_user)
        total, total_order = 0, 0
        order_comprehension = [
            (total := total + j.total, total_order := total_order + j.qty)
            for j in order
        ]
        path = request.META['HTTP_HOST']
        path1 = ['http://' + path + '/media/' + i for i in i.product_images]
        i.product_images = path1
        data = {
            'Product Details': {'Image': i.product_images, 'Name': i.product_name, 'SKU': i.SKU,
                                'Size': i.product_size},
            'Current Stock': i.product_quantity,
            'Growth': {'Orders': total_order, 'Sales': f'₹{total}'},
            'Current Customer Price': i.product_price
        }
        all_product.append(data)
    return JsonResponse({'Message': all_product})


@api_view(['POST'])
def edit_pricing(request):
    primary_key = request.POST['primary_key']
    product_price = request.POST['product_price']
    product_sale_price = request.POST['product_sale_price']
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        product = Product.objects.get(id=primary_key, product_seller=seller_user)
        product.product_price = product_price
        product.product_sale_price = product_sale_price
        product.save()
        return JsonResponse({'Message': 'Price Edit Successfully'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def filter_category(request):
    category = request.POST['category'].upper()
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        product = Product.objects.filter(product_seller=seller_user, product_items=category)
        all_product = []
        for i in product:
            order = Order.objects.filter(product=i, product__product_seller=seller_user)
            total, total_order = 0, 0
            order_comprehension = [
                (total := total + j.total, total_order := total_order + j.qty)
                for j in order
            ]
            path = request.META['HTTP_HOST']
            path1 = ['http://' + path + '/media/' + i for i in i.product_images]
            i.product_images = path1
            data = {
                'Product Details': {'Image': i.product_images, 'Name': i.product_name, 'SKU': i.SKU,
                                    'Size': i.product_size},
                'Current Stock': i.product_quantity,
                'Growth': {'Orders': total_order, 'Sales': f'₹{total}'},
                'Current Customer Price': i.product_price
            }
            all_product.append(data)
        return JsonResponse({'Data': all_product})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def date_growth(request):
    start_time = datetime.time(00, 00, 00)
    end_time = datetime.time(23, 59, 59)
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    try:
        filter_data_list = []
        seller_user = Register.objects.get(email=request.session['email'])
        start_object = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        start_datetime = datetime.datetime(year=start_object.year, month=start_object.month, day=start_object.day,
                                           hour=start_time.hour, minute=start_time.minute, second=start_time.second)
        end_object = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_datetime = datetime.datetime(year=end_object.year, month=end_object.month, day=end_object.day,
                                         hour=end_time.hour, minute=end_time.minute, second=end_time.second)
        filter_data = Product.objects.filter(product_date__range=(start_datetime, end_datetime),
                                             product_seller=seller_user)
        for i in filter_data:
            order = Order.objects.filter(product=i, product__product_seller=seller_user)
            total, total_order = 0, 0
            order_comprehension = [
                (total := total + j.total, total_order := total_order + j.qty)
                for j in order
            ]
            path = request.META['HTTP_HOST']
            path1 = ['http://' + path + '/media/' + i for i in i.product_images]
            i.product_images = path1
            data = {
                'Product Details': {'Image': i.product_images, 'Name': i.product_name, 'SKU': i.SKU,
                                    'Size': i.product_size},
                'Current Stock': i.product_quantity,
                'Growth': {'Orders': total_order, 'Sales': f'₹{total}'},
                'Current Customer Price': i.product_price
            }
            filter_data_list.append(data)
        return JsonResponse({'Filter Order': filter_data_list})

    except Exception as e:
        return JsonResponse({'Message': e.__str__()})
