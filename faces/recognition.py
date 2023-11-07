import os
import numpy as np
import face_recognition
from facerec_shopping_cart.settings import BASE_DIR

def get_faces():
    faces = []
    facesdir = [(folder, BASE_DIR / 'upload' / folder)
                for folder in os.listdir(BASE_DIR / 'upload')]
    
    def get_files(dirname):
        for file in os.listdir(dirname):
            if os.path.isfile(os.path.join(dirname, file)):
                yield file    

    def isNotNone(path):
        return path != None
        
    for facename, facedir in facesdir:
        imgpaths = list(filter(isNotNone, [facedir / file for file in get_files(facedir)]))
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
    
    recognized_names = []
    known_faces_names, known_faces_encodings = known_faces()
    
    unknown_face = face_recognition.load_image_file(unknown_face)
    unknown_face_encodings = face_recognition.face_encodings(unknown_face)
    
    # print('unknown_face: ', len(unknown_face))
    # print('unknown_face_encodings: ', len(unknown_face_encodings))
    
    if len(unknown_face_encodings) > 0:
        
        # unknown_face_encodings = unknown_face_encodings[0]
        
        for unknown_face_enc in unknown_face_encodings:
    
            matches = face_recognition.compare_faces(known_faces_encodings, unknown_face_enc)
            
            face_distances = face_recognition.face_distance(known_faces_encodings, unknown_face_enc)
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index]:
                name = known_faces_names[best_match_index]

            recognized_names.append(name)
            
    return recognized_names if len(recognized_names) > 0 else ['Desconhecido']
    
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