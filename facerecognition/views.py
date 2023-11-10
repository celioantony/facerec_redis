import os
import json
from PIL import Image
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Cart, AddedProducts, Product
from faces.recognition import face_location
from django.contrib import messages
from django.template.loader import render_to_string
from django.template import RequestContext
from faces.training import training

def recognition(request):
    return render(request, 'recognition.html', {})


def training(request):
    return render(request, 'training.html', {})

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