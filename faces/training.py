import os
import face_recognition
import struct
import numpy as np
from facerec_redis.settings import BASE_DIR
from facerec_redis.settings import REDIS_CONN
from .utils import to_redis

client = REDIS_CONN

def get_faces(facename=None, fullpath=None):
    faces = []
    
    facesdir = None
    if facename and fullpath:
        facesdir = [(facename, fullpath)]
    else:
        facesdir = [(folder, BASE_DIR / 'datatraining' / folder)
                    for folder in os.listdir(BASE_DIR / 'datatraining')]

    def get_files(dirname):
        for file in os.listdir(dirname):
            if os.path.isfile(os.path.join(dirname, file)):
                yield file

    def is_not_none(path):
        return path != None
    
    print(facesdir)

    for facename, facedir in facesdir:

        if not client.exists(f'user:{facename}'):
            imgpaths = list(
                filter(is_not_none, [facedir / file for file in get_files(facedir)]))
            faces.append((facename, imgpaths))

    return faces


def training(faces=None):
    
    if not faces:
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

def training_by_user(facename, path):
    faces = get_faces(facename, path)
    training(faces)