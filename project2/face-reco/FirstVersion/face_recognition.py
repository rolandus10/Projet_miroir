import os
import cv2
import numpy as np
faceDetec= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam=cv2.VideoCapture(0)
recognizer= cv2.face.createLBPHFaceRecognizer()
recognizer.load("recognizer/trainingData.yml")
id=0
font = cv2.FONT_HERSHEY_COMPLEX
while(True):
	ret,img=cam.read();
	gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	faces=faceDetec.detectMultiScale(gray,1.3,10)
	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
		# on prédit quel est l'id de la personne à l'écran...
		id,conf=recognizer.predict(gray[y:y+h,x:x+w])
		if id == 1:
			id="patrick"
		elif id==2:
			id="lekemo"
		cv2.putText(img,str(id),(x,y+h), font, 1,(0,255,0),2)
	cv2.imshow("Face",img);
	if (cv2.waitKey(1)==ord('q')):
		break
cam.release()
cv2.destroyAllWindows()
os.system("pause")

