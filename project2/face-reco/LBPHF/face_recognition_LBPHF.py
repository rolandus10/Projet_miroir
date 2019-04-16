import os
import cv2
import numpy as np
faceDetec= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam=cv2.VideoCapture(0)
recognizer= cv2.face.createLBPHFaceRecognizer()
recognizer.load("recognizer/trainingData_LBPHF.yml")
id=0
it=0
dist=0
font = cv2.FONT_HERSHEY_COMPLEX
while(True):
	ret,img=cam.read();
	if not ret: continue
	gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	faces=faceDetec.detectMultiScale(gray,1.4,5)
	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
		collector = cv2.face.StandardCollector_create()
		# on prédit quel est l'id de la personne à l'écran...
		recognizer.predict_collect(gray[y:y+h,x:x+w], collector)
		dist = dist+collector.getMinDist()
		id=collector.getMinLabel()
		it+=1
		if id == 1:
			id="patrick"
		elif id==2:
			id="rosabelle"
		elif id==3:
			id="guy"
		elif id==4:
			id="gilles"
		elif id==5:
			id="flavius"
		elif id==6:
			id="harry"
		cv2.putText(img,str(id),(x,y+h), font, 1,(0,255,0),2)
	cv2.imshow("Face",img);
	if (cv2.waitKey(1)==ord('q')):
		break
cam.release()
cv2.destroyAllWindows()
print("distance moyenne = {}".format(dist/it))
with open('fichier.txt','a') as mon_fichier:
	mon_fichier.write("{}\n".format(dist/it))
dist_moy=0
i=0
with open('fichier.txt','r') as mon_fichier:
	for ligne in mon_fichier.readlines():
		ligne=ligne[0:len(ligne)-len("\n")]
		dist_moy+=float(ligne)
		i+=1
dist_moy=dist_moy/i
print("{}".format(dist_moy))
os.system("pause")

