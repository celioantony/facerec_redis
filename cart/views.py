import os
import json
from PIL import Image
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Cart, AddedProducts
from product.models import Product
from faces.recognition import face_location
from django.contrib import messages
from django.template.loader import render_to_string
from django.template import RequestContext


def cart(request):
    return render(request, 'cart.html', {})


def recognition(request):
    messages.add_message(request, messages.INFO, 'Reconhecimento facial')
    return render(request, 'recognition.html', {})


@csrf_exempt
def face_recognition_image(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if request.method == 'POST' and is_ajax:
        file = request.FILES['file']
        
        recognized_names = face_location(file)

        messages.add_message(request, messages.SUCCESS, 'Reconhecimento processado com sucesso.')
        
        response = dict()
        response['messages'] = render_to_string('messages/ajaxmessages.html', {},  request)
        response['recognized_names'] = recognized_names
        
        return JsonResponse(response)

    return JsonResponse({'message': 'Method not allowed.'})


@csrf_exempt
def create_cart(request):
    try:
        # TODO: change fixed user
        user = User.objects.get(id=1)

        if request.method == 'POST':
            cart = Cart.objects.create(user=user)

            response = {}
            response['data'] = {'cart_id': cart.id}
            response['message'] = 'Cart created successfully.'

            return JsonResponse(response)

    except User.DoesNotExist:
        return JsonResponse({'message': 'Usuário não encontrado.'})


@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        cart_id = body.get('cart_id')
        product_barcode = body.get('product_barcode')

        if not cart_id:
            return JsonResponse({'message': 'Field cart_id is required.'})

        if not product_barcode:
            return JsonResponse({'message': 'Field product_barcode is required.'})

        try:
            cart = Cart.objects.get(id=cart_id)
            product = Product.objects.get(barcode=product_barcode)

            AddedProducts.objects.create(
                cart=cart, product=product, quantity=1, total=product.price)

            return JsonResponse({'message': 'Product added successfully.'})

        except Cart.DoesNotExist:
            return JsonResponse({'message': 'Cart does not exist.'})
        except Product.DoesNotExist:
            return JsonResponse({'message': 'Product does not exist.'})


@csrf_exempt
def increase_quantity(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        cart_id = body.get('cart_id')
        product_barcode = body.get('product_barcode')

        if not cart_id:
            return JsonResponse({'message': 'Field cart_id is required.'})

        if not product_barcode:
            return JsonResponse({'message': 'Field product_barcode is required.'})

        try:
            product = Product.objects.get(barcode=product_barcode)
            added_product = AddedProducts.objects.get(
                cart=cart_id, product=product.id)

            # increase
            added_product.quantity = added_product.quantity + 1
            added_product.total = product.price * added_product.quantity
            added_product.save()

            return JsonResponse({'message': 'Product increase.'})

        except Product.DoesNotExist:
            return JsonResponse({'message': 'Product does not exist.'})
        except AddedProducts.DoesNotExist:
            return JsonResponse({'message': 'Product Added does not exists.'})


@csrf_exempt
def decrease_quantity(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        cart_id = body.get('cart_id')
        product_barcode = body.get('product_barcode')

        if not cart_id:
            return JsonResponse({'message': 'Field cart_id is required.'})

        if not product_barcode:
            return JsonResponse({'message': 'Field product_barcode is required.'})

        try:
            product = Product.objects.get(barcode=product_barcode)
            added_product = AddedProducts.objects.get(
                cart=cart_id, product=product.id)

            # decrease
            if added_product.quantity > 1:
                added_product.quantity = added_product.quantity - 1
                added_product.total = product.price * added_product.quantity
                added_product.save()

                return JsonResponse({'message': 'Product decrease.'})
            else:
                return JsonResponse({'message': 'Product decrease not allowed.'})

        except Product.DoesNotExist:
            return JsonResponse({'message': 'Product does not exist.'})
        except AddedProducts.DoesNotExist:
            return JsonResponse({'message': 'Product Added does not exists.'})
