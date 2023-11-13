import os
import base64
from PIL import Image
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from faces.recognition import face_location
from django.contrib import messages
from django.template.loader import render_to_string
from facerec_redis.settings import BASE_DIR
from faces.training import training_by_user

def recognition(request):
    return render(request, 'recognition.html', {})


def training(request):
    return render(request, 'training.html', {})


@csrf_exempt
def face_upload_training(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if request.method == 'POST' and is_ajax:
        
        facename = request.POST.get('facename') or None        
        files = request.FILES.getlist('files[]')
        
        facename = '_'.join(facename.split(' '))
        fullpath = BASE_DIR / 'datatraining' / facename
        
        if not os.path.exists(fullpath):
            os.makedirs(fullpath)
        
        for index, file in enumerate(files, start=0):
            img = Image.open(file)
            img.save(fullpath / f'face{index:03}.png')
            
        # training redis
        training_by_user(facename, fullpath)

        messages.add_message(request, messages.SUCCESS, 'Trainamento finalizado.')
        
        response = dict()
        response['messages'] = render_to_string('messages/ajaxmessages.html', {},  request)
        
        return JsonResponse(response)

    return JsonResponse({'message': 'Method not allowed.'})

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