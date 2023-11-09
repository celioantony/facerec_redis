import os
import face_recognition
import struct
import numpy as np
from facerec_shopping_cart.settings import BASE_DIR
from facerec_shopping_cart.settings import REDIS_CONN
from .utils import to_redis

client = REDIS_CONN

def get_faces():
    faces = []
    facesdir = [(folder, BASE_DIR / 'upload' / folder)
                for folder in os.listdir(BASE_DIR / 'upload')]

    def get_files(dirname):
        for file in os.listdir(dirname):
            if os.path.isfile(os.path.join(dirname, file)):
                yield file

    def is_not_none(path):
        return path != None

    for facename, facedir in facesdir:

        if not client.exists(f'user:{facename}'):
            imgpaths = list(
                filter(is_not_none, [facedir / file for file in get_files(facedir)]))
            faces.append((facename, imgpaths))

    return faces


def training():
    faces = get_faces()

    for facename, facepaths in faces:
        hkey = f'faces:{facename}'
        for i, imgpath in enumerate(facepaths, start=1):
            image = face_recognition.load_image_file(imgpath)
            face_encoding = face_recognition.face_encodings(image)

            if len(face_encoding) > 0:
                face_encoding = face_encoding[0]

                mapkey = f'img:{i:03}'
                # persiste treining to redis
                encoded = to_redis(face_encoding)
                client.hset(hkey, mapping={mapkey: encoded})
