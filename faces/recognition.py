import os
import numpy as np
import face_recognition
from facerec_redis.settings import BASE_DIR
from facerec_redis.settings import REDIS_CONN
from .utils import bytes_to_nparray

client = REDIS_CONN


def get_faces():
    faces = []
    facesdir = [(folder, BASE_DIR / 'datatraining' / folder)
                for folder in os.listdir(BASE_DIR / 'datatraining')]

    def get_files(dirname):
        for file in os.listdir(dirname):
            if os.path.isfile(os.path.join(dirname, file)):
                yield file

    def isNotNone(path):
        return path != None

    for facename, facedir in facesdir:
        imgpaths = list(
            filter(isNotNone, [facedir / file for file in get_files(facedir)]))
        faces.append((facename, imgpaths))

    return faces


def known_faces():
    faces = get_faces()

    known_faces_encodings = []
    known_faces_names = []

    for facename, facepaths in faces:

        name = str.title(' '.join(facename.split('_')))

        for imgpath in facepaths:
            image = face_recognition.load_image_file(imgpath)
            face_encoding = face_recognition.face_encodings(image)

            if len(face_encoding) > 0:
                face_encoding = face_encoding[0]

                known_faces_names.append(name)
                known_faces_encodings.append(face_encoding)

    return (known_faces_names, known_faces_encodings)


def face_location(unknown_face):

    faces_keys_iter = client.scan_iter('faces:*')

    def get_name(hkey):
        partial_key = hkey.decode('utf-8').split(':')[1]
        return str.title(' '.join(partial_key.split('_')))

    faces_map = dict()
    known_faces_names_index = []
    known_faces_encodings = []
    for index, hkey in enumerate(faces_keys_iter, start=0):
        faces_map[index] = get_name(hkey)

        img_faces_iter = client.hscan_iter(hkey, 'img:*')
        for mapkey, face_encoding_bytes in img_faces_iter:
            face_encoding = bytes_to_nparray(face_encoding_bytes)
            known_faces_names_index.append(index)
            known_faces_encodings.append(face_encoding)

    recognized = []
    # known_faces_names, known_faces_encodings = known_faces()

    unknown_face = face_recognition.load_image_file(unknown_face)
    unknown_face_encodings = face_recognition.face_encodings(unknown_face)

    if len(unknown_face_encodings) > 0:

        unknown_face_encodings = unknown_face_encodings

        for unknown_face_enc in unknown_face_encodings:
            name = 'Desconhecido'
            matches = face_recognition.compare_faces(
                known_faces_encodings, unknown_face_enc)
            face_distances = face_recognition.face_distance(
                known_faces_encodings, unknown_face_enc)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index] and \
                (known_faces_names_index[best_match_index] in known_faces_names_index):
                name = faces_map[known_faces_names_index[best_match_index]]
            
            recognized.append(name)

    return recognized if len(recognized) > 0 else ['Desconhecido']

    # print('len: ')
    # print(len(unknown_face), len(unknown_face_encodings))

    # face_names = []

    # for (top, right, bottom, left), face_encoding in zip(unknown_face_locations, unknown_face_encodings):

    #     matches = face_recognition.compare_faces(known_faces_encodings, face_encoding)

    #     name = 'Unknown'

    #     face_distances = face_recognition.face_distance(known_faces_encodings, face_encoding)
    #     best_match_index = np.argmin(face_distances)
    #     if matches[best_match_index]:
    #         name = known_faces_names[best_match_index]

    #     face_names.append(name)
