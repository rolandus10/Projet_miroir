import os
import cv2
import numpy as np
# on va sauvegarder 20 photos 
faceDetec= cv2.CascadeClassifier('haarcascade_frontalface_default.xml');

cam=cv2.VideoCapture(0);

id=input('enter user id')
i=0;
while(True):
        #print('read')
        ret,img=cam.read();
        #if not ret: continue 
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceDetec.detectMultiScale(gray,1.3,5);
        for (x,y,w,h) in faces:
                i+=1;
                #il faut que le fichier dataSet existe déjà...
		# on enregistre l'image dans le fichier dataSet sous le nom User.id.i.jpg
		#gray[y:y+h,x:x+w] est l'image croppée on ne sauve que le visage.
                print('write')
                cv2.imwrite("dataSet/User."+str(id)+"."+str(i)+".jpg",gray[y:y+h,x:x+w])
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                # on attend 30 milli secondes pour pouvoir changer de tête grimace, profil, avec lunettes,...
                cv2.waitKey(30);
        cv2.imshow("Face",img);
        cv2.waitKey(1)
        if (i>=70):
                break
cam.release()
cv2.destroyAllWindows()
