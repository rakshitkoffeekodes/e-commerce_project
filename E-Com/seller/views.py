import os
import datetime
import random
import openpyxl
import xlsxwriter
from django.core.files.storage import default_storage
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password
from .serilizers import *
from django.conf import settings
from django.core.mail import send_mail
from base.serlializers import *


# Create your views here.


@api_view(['POST'])
def register(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    try:
        if password == confirm_password:
            global user_otp, temp
            user_otp = random.randint(100000, 999999)
            subject = 'One Time Password (OTP) Confirmation'
            message = f'''Hi {first_name} {last_name},
                        This email confirms your one-time password (OTP) for E-Commerce Site.
                        Your OTP is: {user_otp}
                        Thank you,
                        E-Commerce Site'''
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail(subject, message, email_from, recipient_list)
            temp = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password
            }
            return JsonResponse({'Message': 'OTP Sending Successfully.'})
        else:
            return JsonResponse({'Message': 'Password Not Match.'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def otp_verification(request):
    otp = request.POST['otp']
    try:
        if user_otp == int(otp):
            Register.objects.create(
                first_name=temp["first_name"],
                last_name=temp["last_name"],
                email=temp["email"],
                password=make_password(temp["password"])
            )
            return JsonResponse({'Message': 'Register Success'})
        else:
            return JsonResponse({'Message': 'OTP is not match.'})
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
            return JsonResponse({'Message': 'Login Successfully.'})
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
        serial = RegisterSerializer(seller_user)
        return JsonResponse({'Profile': serial.data, 'Profile Image': path1})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['PUT'])
def update_profile(request):
    profile_picture = request.FILES.get('profile_image', '')
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
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
    product_category = request.POST['product_category'].upper()
    product_sub_category = request.POST['product_sub_category'].upper()
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
        product_id = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H"]
        id1 = random.choices(product_id, k=9)
        product = "".join(id1)
        product_image = [
            default_storage.save(os.path.join(settings.MEDIA_ROOT, 'Product', image.name.replace(' ', '_')), image)
            for image in product_images]
        path = request.META['HTTP_HOST']
        path1 = ['http://' + path + '/media/' + i for i in product_image]
        product_add = Product()
        product_add.product_category = product_category
        product_add.product_sub_category = product_sub_category
        product_add.product_images = path1
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
        product_add.product = product
        product_add.product_seller = seller_user
        product_add.save()
        return JsonResponse({'message': 'Product Add Successfully.'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def bulk_upload_catalog(request):
    product_category = request.POST['product_category'].upper()
    product_sub_category = request.POST['product_sub_category'].upper()
    product_image = request.FILES.getlist('product_image')
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        name = random.randint(00000, 99999)
        workbook = xlsxwriter.Workbook(f'D:\\Task\\E-Com\\media\\file\\Bulk-Catalog-{name}.xlsx')
        worksheet = workbook.add_worksheet()
        product_image = [
            default_storage.save(os.path.join(settings.MEDIA_ROOT, 'Product', image.name.replace(' ', '_')), image)
            for image in product_image]
        path = request.META['HTTP_HOST']
        path1 = ['http://' + path + '/media/' + i for i in product_image]
        expenses = (
            'Images1', 'Images2', 'Images3', 'Images4', 'SKU', 'Name', 'Price', 'Sale Price', 'Quantity',
            'product_category', 'product_sub_category', 'Branding',
            'Tags', 'Size', 'Color', 'Fabric', 'Description')

        row = 1
        for col_num, value in enumerate(expenses):
            for index, i in enumerate(path1):
                if value == 'product_category':
                    worksheet.write(0, col_num, value)
                    worksheet.write(row + index, col_num, product_category)
                elif value == 'product_sub_category':
                    worksheet.write(0, col_num, value)
                    worksheet.write(row + index, col_num, product_sub_category)
                elif value == 'Images1':
                    worksheet.write(0, col_num, value)
                    worksheet.write(row + index, col_num, i)
                worksheet.write(0, col_num, value)
        path = request.META['HTTP_HOST']
        path2 = ['http://' + path + '/media/file/' + f'Bulk-Catalog-{name}.xlsx']
        workbook.close()
        return JsonResponse({'Execl File Link': path2})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def get_image_link(request):
    upload_image = request.FILES.getlist('upload_image')
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        product_image = [
            default_storage.save(os.path.join(settings.MEDIA_ROOT, 'Product', image.name.replace(' ', '_')), image)
            for image in upload_image]
        path = request.META['HTTP_HOST']
        path1 = ['http://' + path + '/media/' + i for index, i in enumerate(product_image)]
        return JsonResponse({'Message': path1})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def upload_catalog_file(request):
    upload_file = request.FILES['upload_file']
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        directory = 'D:\\Task\\E-Com\\media\\file'
        file_path = os.path.join(directory, str(upload_file))
        if os.path.exists(file_path):
            wb = openpyxl.load_workbook(upload_file)
            ws = wb.active
            max_row = ws.max_row
            for i in range(2, max_row + 1):
                row = ws[i]
                image_links = []
                for cell in row:
                    if cell.value and ('http' in str(cell.value) in str(cell.value)):
                        image_links.append(str(cell.value))
                p_id = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H"]
                id2 = random.choices(p_id, k=9)
                product = "".join(id2)
                product_add = Product()
                product_add.product_images = image_links
                product_add.SKU = row[4].value
                product_add.product_name = row[5].value
                product_add.product_price = row[6].value
                product_add.product_sale_price = row[7].value
                product_add.product_quantity = row[8].value
                product_add.product_category = row[9].value
                product_add.product_sub_category = row[10].value
                product_add.product_branding = row[11].value
                product_add.product_tags = row[12].value
                product_add.product_size = row[13].value
                product_add.product_color = row[14].value
                product_add.product_fabric = row[15].value
                product_add.product_description = row[16].value
                product_add.product_date = datetime.datetime.now()
                product_add.product = product
                product_add.product_seller = seller_user
                product_add.save()
            return JsonResponse({'Message': 'Bulk Catalog Upload Successfully.'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['GET'])
def view_all_product(request):
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        all_product = Product.objects.filter(product_seller=seller_user)
        serial = ProductSerializer(all_product, many=True)
        for view in serial.data:
            view.pop('id')
            view.pop('product_sale_price')
            view.pop('product_quantity')
            view.pop('product_sub_category')
            view.pop('product_branding')
            view.pop('product_tags')
            view.pop('product_fabric')
            view.pop('product_description')
            view.pop('product')
            view.pop('product_seller')
        return JsonResponse({'Message': 'All Product', 'Products': serial.data})
    except Exception as e:
        return JsonResponse({'Message': e.__str__(), 'Products': None})


def product_update(request, update, product_images, SKU, product_name, product_branding, product_tags,
                   product_color, product_fabric, product_description):
    if len(product_images) != 0:
        product_image = [
            default_storage.save(os.path.join(settings.MEDIA_ROOT, 'Product', image.name.replace(' ', '_')), image)
            for image in product_images]
        path = request.META['HTTP_HOST']
        path1 = ['http://' + path + '/media/' + i for i in product_image]
        if not product_images == '':
            update.product_images = path1
        if not SKU == '':
            update.SKU = SKU
        if not product_name == '':
            update.product_name = product_name
        if not product_branding == '':
            update.product_branding = product_branding
        if not product_tags == '':
            update.product_tags = product_tags
        if not product_color == '':
            update.product_color = product_color
        if not product_fabric == '':
            update.product_fabric = product_fabric
        if not product_description == '':
            update.product_description = product_description
    else:
        if not SKU == '':
            update.SKU = SKU
        if not product_name == '':
            update.product_name = product_name
        if not product_branding == '':
            update.product_branding = product_branding
        if not product_tags == '':
            update.product_tags = product_tags
        if not product_color == '':
            update.product_color = product_color
        if not product_fabric == '':
            update.product_fabric = product_fabric
        if not product_description == '':
            update.product_description = product_description
    update.save()
    return update


@api_view(['PUT'])
def update_product(request):
    primary_key = request.POST['primary_key']
    product_images = request.FILES.getlist('product_images')
    SKU = request.POST.get('SKU')
    product_name = request.POST.get('product_name')
    product_branding = request.POST.get('product_branding')
    product_tags = request.POST.get('product_tags')
    product_color = request.POST.get('product_color')
    product_fabric = request.POST.get('product_fabric')
    product_description = request.POST.get('product_description')
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        update = Product.objects.get(product_seller=seller_user, id=primary_key)
        update_data = {
            'Data': product_update(request, update, product_images, SKU, product_name, product_branding, product_tags,
                                   product_color, product_fabric, product_description)}
        return JsonResponse({'Message': 'Update Product Successfully.'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['DELETE'])
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
def inventory(request):
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        all_catalog = Product.objects.filter(product_seller=seller_user)
        serial = ProductSerializer(all_catalog, many=True)
        for data in serial.data:
            data.pop('id')
            data.pop('product_sale_price')
            data.pop('product_category')
            data.pop('product_sub_category')
            data.pop('product_branding')
            data.pop('product_tags')
            data.pop('product_color')
            data.pop('product_fabric')
            data.pop('product_description')
            data.pop('product_date')
            data.pop('product')
            data.pop('product_seller')
        return JsonResponse({'Message': 'Filter Category', 'Stock': serial.data})
    except Exception as e:
        return JsonResponse({'Message': e.__str__(), 'Stock': None})


@api_view(['POST'])
def edit_stock(request):
    primary_key = request.POST['primary_key']
    stock = request.POST['stock']
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        stock_edit = Product.objects.get(product_seller=seller_user, id=primary_key)
        stock_edit.product_quantity = stock
        stock_edit.save()
        return JsonResponse({'Message': 'Stock Edit Successfully.'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def inventory_filter_category(request):
    category = request.POST['category'].upper()
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        category_filter = Product.objects.filter(product_seller=seller_user, product_category=category)
        serial = ProductSerializer(category_filter, many=True)
        if len(category_filter) != 0:
            for data in serial.data:
                data.pop('id')
                data.pop('product_sale_price')
                data.pop('product_category')
                data.pop('product_sub_category')
                data.pop('product_branding')
                data.pop('product_tags')
                data.pop('product_color')
                data.pop('product_fabric')
                data.pop('product_description')
                data.pop('product_date')
                data.pop('product')
                data.pop('product_seller')
            return JsonResponse({'Message': 'Filter Category', 'Data': serial.data})
        else:
            return JsonResponse({'Message': 'Category is Not exist', 'Data': None})
    except Exception as e:
        return JsonResponse({'Message': e.__str__(), 'Data': None})


@api_view(['POST'])
def inventory_edit_catalog(request):
    primary_key = request.POST['primary_key']
    product_images = request.FILES.getlist('product_images')
    SKU = request.POST.get('SKU')
    product_name = request.POST.get('product_name')
    product_branding = request.POST.get('product_branding')
    product_tags = request.POST.get('product_tags')
    product_color = request.POST.get('product_color')
    product_fabric = request.POST.get('product_fabric')
    product_description = request.POST.get('product_description')
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        update = Product.objects.get(product_seller=seller_user, id=primary_key)
        update_data = {
            'Data': product_update(request, update, product_images, SKU, product_name, product_branding, product_tags,
                                   product_color, product_fabric, product_description)}
        return JsonResponse({'Message': 'Edit Catalog Successfully.'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


def order_data(view_all_order):
    all_order = [{'Order ID': i.order,
                  'Image': i.details.cart.product.product_images,
                  'Name': i.details.cart.product.product_name,
                  'SKU ID': i.details.cart.product.SKU,
                  'Company ID': i.company,
                  'Quantity': i.details.cart.qty,
                  'Size': i.details.cart.product.product_size,
                  'Dispatch Date/ SLA': i.dispatch_date}
                 for i in view_all_order]
    return all_order


@api_view(['GET'])
def pending_order(request):
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        buyer_order = Payment.objects.filter(details__cart__status=True)
        buyer_all_order = Order.objects.filter(details__cart__product__product_seller=seller_user,
                                               details__status=True).only('order')
        list2 = [i.order for i in buyer_all_order]
        for i in buyer_order:
            if i.order not in list2:
                company_id = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H"]
                id2 = random.choices(company_id, k=9)
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
        all_order = order_data(view_all_order)
        return JsonResponse({'Message': 'View All Pending Order', 'View All Order': all_order})
    except Exception as e:
        return JsonResponse({'Message': e.__str__(), 'View All Order': None})


@api_view(['POST'])
def filter_order_date(request):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    start_time = datetime.time(00, 00, 00)
    end_time = datetime.time(23, 59, 59)
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        start_object = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        start_datetime = datetime.datetime(year=start_object.year, month=start_object.month, day=start_object.day,
                                           hour=start_time.hour, minute=start_time.minute, second=start_time.second)
        end_object = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_datetime = datetime.datetime(year=end_object.year, month=end_object.month, day=end_object.day,
                                         hour=end_time.hour, minute=end_time.minute, second=end_time.second)
        view_all_order = Order.objects.filter(order_date__range=(start_datetime, end_datetime),
                                              details__cart__product__product_seller=seller_user,
                                              details__cart__status=True, status=True)
        filter_data_list = order_data(view_all_order)
        return JsonResponse({'Message': 'Filter By: Order Date', 'Filter Order': filter_data_list})

    except Exception as e:
        return JsonResponse({'Message': e.__str__(), 'Filter Order': None})


@api_view(['POST'])
def filter_dispatch_date(request):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    start_time = datetime.time(00, 00, 00)
    end_time = datetime.time(23, 59, 59)
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        start_object = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        start_datetime = datetime.datetime(year=start_object.year, month=start_object.month, day=start_object.day,
                                           hour=start_time.hour, minute=start_time.minute, second=start_time.second)
        end_object = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_datetime = datetime.datetime(year=end_object.year, month=end_object.month, day=end_object.day,
                                         hour=end_time.hour, minute=end_time.minute, second=end_time.second)
        view_all_order = Order.objects.filter(dispatch_date__range=(start_datetime, end_datetime),
                                              details__cart__product__product_seller=seller_user,
                                              details__cart__status=True, status=True)
        filter_data_list = order_data(view_all_order)
        return JsonResponse({'Message': 'Filter By: Dispatch Date', 'Filter Order': filter_data_list})

    except Exception as e:
        return JsonResponse({'Message': e.__str__(), 'Filter Order': None})


@api_view(['POST'])
def order_search(request):
    search = request.POST.get('search', '')
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        view_all_order = Order.objects.filter(
            Q(order__icontains=search) | Q(company__icontains=search) | Q(
                details__cart__product__SKU__icontains=search),
            details__cart__product__product_seller=seller_user, status=True)
        if view_all_order.count() != 0 and search != '':
            search_data = order_data(view_all_order)
            return JsonResponse({'Message1': 'Search Order', 'Message2': 'Search Order Only SKU, Order ID, Company ID',
                                 'Search Order': search_data})
        else:
            return JsonResponse({'Message': 'Product Is Not Found', 'Search Order': None})
    except Exception as e:
        return JsonResponse({'Message': e.__str__(), 'Search Order': None})


def accept_data(accept):
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
    return accept


@api_view(['POST'])
def order_accept(request):
    primary_key = request.POST['primary_key']
    id_list = primary_key.split(',')
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        if not len(id_list) > 1:
            accept = Order.objects.get(id=primary_key, status=True, details__cart__product__product_seller=seller_user)
            accept_order = {'Accept': accept_data(accept)}
            return JsonResponse({'Message': 'Order Accept'})
        else:
            for i in id_list:
                accept = Order.objects.get(id=i, status=True, details__cart__product__product_seller=seller_user)
                accept_order = {'Accept': accept_data(accept)}
            return JsonResponse({'Message': 'Order Accept'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['GET'])
def ready_to_ship(request):
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        view_accept_all_order = Accept.objects.filter(status=True, order__product__product_seller=seller_user)
        accept_orders = [{
            'Order ID': i.order.order,
            'Image': i.product.product_images,
            'Name': i.product.product_name,
            'SKU ID': i.product.SKU,
            'Company ID': i.order.company,
            'Quantity': i.qty,
            'Size': i.product.product_size,
            'Dispatch Date/ SLA': f"{i.order.dispatch_date.day} {i.order.dispatch_date.strftime('%b')}'{i.order.dispatch_date.strftime('%y')}"
        } for i in view_accept_all_order]
        return JsonResponse({'Message': 'Ready To Ship', 'Accept Orders': accept_orders})
    except Exception as e:
        return JsonResponse({'Message': e.__str__(), 'Accept Orders': None})


def label_data(label, seller_user, purchase_order_no, invoice_no, invoice_date, total, tax):
    data = {
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
            data = label_data(label, seller_user, purchase_order_no, invoice_no, invoice_date, total, tax)
            return JsonResponse({'Message': 'Shipping Label', 'Label Data': data})

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
                data = label_data(label, seller_user, purchase_order_no, invoice_no, invoice_date, total, tax)
                data_list.append(data)
            return JsonResponse({'Message': 'Shipping Label', 'Label Data': data_list})
    except Exception as e:
        return JsonResponse({'Message': e.__str__(), 'Label Data': None})


def cancel_data(cancel):
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
    return cancel


@api_view(['POST'])
def cancel_order(request):
    primary_key = request.POST['primary_key']
    id_list = primary_key.split(',')
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        if not len(id_list) > 1:
            cancel = Order.objects.get(id=primary_key, status=True, details__cart__product__product_seller=seller_user)
            order_cancel = cancel_data(cancel)
            return JsonResponse({'Message': 'Order Cancel'})
        else:
            for i in id_list:
                cancel = Order.objects.get(id=i, status=True, details__cart__product__product_seller=seller_user)
                order_cancel = cancel_data(cancel)
            return JsonResponse({'Message': 'Order Cancel'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['GET'])
def cancelled(request):
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        view_cancel_all_order = Cancel.objects.filter(status=True, order__product__product_seller=seller_user)
        cancel_orders = [{
            'Image': i.product.product_images,
            'Name': i.product.product_name,
            'Order ID': i.order.order,
            'SKU ID': i.product.SKU,
            'Company ID': i.order.company,
            'Quantity': i.qty,
            'Size': i.product.product_size,
        } for i in view_cancel_all_order]
        return JsonResponse({'Message': 'View Cancelled', 'Cancel Order': cancel_orders})
    except Exception as e:
        return JsonResponse({'Message': e.__str__(), 'Cancel Order': None})


def pricing_data(product, seller_user):
    all_product = []
    for i in product:
        order = Order.objects.filter(product=i, product__product_seller=seller_user)
        total, total_order = 0, 0
        order_comprehension = [
            (total := total + j.total, total_order := total_order + j.qty)
            for j in order
        ]
        data = {
            'Product Details': {'Image': i.product_images, 'Name': i.product_name, 'SKU': i.SKU,
                                'Size': i.product_size},
            'Current Stock': i.product_quantity,
            'Growth': {'Orders': total_order, 'Sales': f'₹{total}'},
            'Current Customer Price': i.product_price
        }
        all_product.append(data)
    return all_product


@api_view(['GET'])
def pricing(request):
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        product = Product.objects.filter(product_seller=seller_user)
        all_product = pricing_data(product, seller_user)
        return JsonResponse({'Message': 'Pricing', 'Product': all_product})
    except Exception as e:
        return JsonResponse({'Message': e.__str__(), 'Product': None})


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
        product = Product.objects.filter(product_seller=seller_user, product_sub_category=category)
        all_product = pricing_data(product, seller_user)
        return JsonResponse({'Message': 'Filter By: Category', 'Product': all_product})
    except Exception as e:
        return JsonResponse({'Message': e.__str__(), 'Product': None})


@api_view(['POST'])
def date_growth(request):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    start_time = datetime.time(00, 00, 00)
    end_time = datetime.time(23, 59, 59)
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        start_object = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        start_datetime = datetime.datetime(year=start_object.year, month=start_object.month, day=start_object.day,
                                           hour=start_time.hour, minute=start_time.minute, second=start_time.second)
        end_object = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_datetime = datetime.datetime(year=end_object.year, month=end_object.month, day=end_object.day,
                                         hour=end_time.hour, minute=end_time.minute, second=end_time.second)
        product = Product.objects.filter(product_date__range=(start_datetime, end_datetime),
                                         product_seller=seller_user)
        all_product = pricing_data(product, seller_user)
        return JsonResponse({'Message': 'Date Growth', 'Growth Product': all_product})
    except Exception as e:
        return JsonResponse({'Message': e.__str__(), 'Growth Product': None})


def return_data(return_order):
    all_returns = [{
        'Images': i.order.cart.product.product_images,
        'Name': i.order.cart.product.product_name,
        'SKU ID': i.order.cart.product.SKU,
        'Category': i.order.cart.product.product_category,
        'Qty': i.order.cart.qty,
        'Size': i.order.cart.product_size,
        'Order ID': i.order.order,
        'Return Reason': i.order_return_message,
        'Return Shipping Fee': f'₹{i.return_shipping_Fee}',
        'Created Date': f"{i.return_date.day} {i.return_date.strftime('%b')}'{i.return_date.strftime('%y')}",
        'Return ID': i.returns,
    } for i in return_order]
    return all_returns


@api_view(['GET'])
def return_tracking(request):
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        return_order = Return.objects.filter(order__cart__product__product_seller=seller_user)
        all_returns = return_data(return_order)
        return JsonResponse({'Message': 'Tracking Return', 'Return Product': all_returns})
    except Exception as e:
        return JsonResponse({'Message': e.__str__(), 'Return Product': None})


@api_view(['GET'])
def return_overview(request):
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        product = Product.objects.filter(product_seller=seller_user)
        all_returns = []
        for i in product:
            return_order = Return.objects.filter(order__cart__product__product_seller=seller_user,
                                                 order__cart__product__product=i.product)
            order = Accept.objects.filter(product__product=i.product, product__product_seller=seller_user)
            total, total_order = 0, 0
            for k in order:
                total_order += k.qty
            for _ in return_order:
                total += 1
            if total != 0 and total_order != 0:
                data = {
                    'Image': i.product_images,
                    'Name': i.product_name,
                    'Category': i.product_category,
                    'Return Order': total,
                    'Returns': f'{round(total * 100 / total_order, 1)}%',
                }
                all_returns.append(data)
            else:
                data = {
                    'Image': i.product_images,
                    'Name': i.product_name,
                    'Category': i.product_category,
                    'Return Order': '-',
                    'Returns': '0.0%',
                }
                all_returns.append(data)
        return JsonResponse({'Message': 'Return Over View', 'returns': all_returns})
    except Exception as e:
        return JsonResponse({'Message': e.__str__(), 'returns': None})


@api_view(['POST'])
def return_filter_category(request):
    category = request.POST['category']
    try:
        seller_user = Register.objects.get(email=request.session['email'])
        return_order = Return.objects.filter(order__cart__product__product_seller=seller_user,
                                             order__cart__product__product_category=category)
        all_returns = return_data(return_order)
        return JsonResponse({'Message': 'Filter By: Category', 'Filter Data': all_returns})
    except Exception as e:
        return JsonResponse({'Message': e.__str__(), 'Filter Data': None})


@api_view(['POST'])
def return_filter_date(request):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    start_time = datetime.time(00, 00, 00)
    end_time = datetime.time(23, 59, 59)
    try:

        seller_user = Register.objects.get(email=request.session['email'])
        start_object = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        start_datetime = datetime.datetime(year=start_object.year, month=start_object.month, day=start_object.day,
                                           hour=start_time.hour, minute=start_time.minute, second=start_time.second)
        end_object = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_datetime = datetime.datetime(year=end_object.year, month=end_object.month, day=end_object.day,
                                         hour=end_time.hour, minute=end_time.minute, second=end_time.second)
        return_order = Return.objects.filter(return_date__range=(start_datetime, end_datetime),
                                             order__cart__product__product_seller=seller_user)
        all_returns = return_data(return_order)
        return JsonResponse({'Message': 'Filter By: Return Date', 'Filter Data': all_returns})
    except Exception as e:
        return JsonResponse({'Message': e.__str__(), 'Filter Data': None})
