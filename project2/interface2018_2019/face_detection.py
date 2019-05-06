import os
import cv2
import numpy as np
id=0
def detection():
	# le fichier haarcascade_frontalface_default.xml doit être dans le dossier où est sauvegardé le code
	faceDetec= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

	# 0 correspond en général à la webcam si ça ne marche pas il faut tester d'autres numéros
	cam=cv2.VideoCapture(0)
	# on va capter frame par frame 
	font = cv2.FONT_HERSHEY_COMPLEX

	while(True):
		ret,img=cam.read()
		#img est une image en couleur
		gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		# il est possible d'ajouter un attribut qui donne la taille minimum du rectangle--> (minSize=(50, 50))
		faces=faceDetec.detectMultiScale(gray,1.3,10)
		for (x,y,w,h) in faces:
			# (0,0,255) rouge  (0,255,0) vert (255,0,0) bleu
			# le dernier nombre (2) correspond à l'épaisseur du trait
			cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
		# Write some Text
		texte="Found "+str(len(faces))+ " faces"
		id=len(faces)
		print(id)
		cv2.putText(img,texte,(10,20), font, 0.75,(0,255,0),1)
		cv2.imshow("Face",img)
		# waitKey est indispenssable pour que open cv fonctionne (fait attendre 1 milliseconde)
		if (cv2.waitKey(1)==ord('q')):
			break
detect=detection()
#♀print(id)
cam.release()
cv2.destroyAllWindows()
os.system("pause")
