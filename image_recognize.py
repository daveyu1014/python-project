# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 21:32:43 2022

@author: dave7
"""

import face_recognition
#image = face_recognition.load_image_file("your_file.jpg")
#face_locations = face_recognition.face_locations(image)
#face_landmarks_list = face_recognition.face_landmarks(image)

picture_of_me = face_recognition.load_image_file("me.jpg")
my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

unknown_picture = face_recognition.load_image_file("unkknow.jpg")
unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)

if results[0] == True:
    print("It's a picture of me!")
else:
    print("It's not a picture of me!")