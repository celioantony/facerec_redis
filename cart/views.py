import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Cart, AddedProducts
from product.models import Product


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
