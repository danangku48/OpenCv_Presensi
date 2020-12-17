import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
from time import sleep
from datetime import datetime
import pandas as pd
import datetime as dt

def data_train():

    train = {}

    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("faces/" + f)
                encoding = fr.face_encodings(face)[0]
                train[f.split(".")[0]] = encoding

    return train


def unknown(img):

    face = fr.load_image_file("faces/" + img)
    encoding = fr.face_encodings(face)[0]

    return encoding


def classify_face():

    faces = data_train()
    faces_train = list(faces.values())
    known_face_names = list(faces.keys())

    cap=cv2.VideoCapture(1)

    while True:
    #img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    #img = img[:,:,::-1]
        ret,img=cap.read()
        face_locations = face_recognition.face_locations(img)
        unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

        face_names = []
        for face_encoding in unknown_face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(faces_train, face_encoding)
            name = "Unknown"

            # use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(faces_train, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

            tanggal=dt.datetime.today().date()
            waktu=datetime.now().strftime("%H:%M")
            print(waktu)
            print(name)
            print('Done!')
  #          print(waktu)
 #           print(name)
            #cv2.imshow('img',img)
            df=pd.read_excel('Daftar Hadir.xlsx')
            df2=df.append({'Tanggal':tanggal,'Nama':name,'Datang':waktu},ignore_index=True)
            df2.to_excel("Daftar Hadir.xlsx",index= False)
            break
        break


   
while True:
    input('press Enter to Attendance:')
    print('Recognize')
    classify_face()



