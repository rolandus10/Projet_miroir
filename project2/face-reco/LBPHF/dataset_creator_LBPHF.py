import os
import cv2
import numpy as np
id=input('enter user id')
faceDetec= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam=cv2.VideoCapture(0)
numPict=20
i=0
directory="dataSet_LBPHF"
if not os.path.exists(directory):
    os.makedirs(directory)
directory=directory+"/"+str(id)
# on fait un fichier par personne
if not os.path.exists(directory):
    os.makedirs(directory)
if os.path.isfile(directory+'/fichier.txt'):
	with open(directory+'/fichier.txt','r') as mon_fichier:
		contenu=mon_fichier.read()
		pos1=contenu.find(',numPict= ')
		i=int(contenu[pos1+len(',numPict= '):])
numPict+=i
def capture():
	while(True):
		ret,img=cam.read();
		gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		faces=faceDetec.detectMultiScale(gray,1.4,5)		
		for (x,y,w,h) in faces:
			i+=1
			# on enregistre l'image dans le fichier dataSet sous le nom User.id.i.jpg
			#gray[y:y+h,x:x+w] est l'image croppée on ne sauve que le visage.
			cv2.imwrite(directory+"/User."+str(id)+"."+str(i)+".jpg",gray[y:y+h,x:x+w])
			cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
			# on attend 250 milli secondes pour pouvoir changer de tête grimace, profil, avec lunettes,...
			cv2.waitKey(250)
		cv2.imshow("Face",img);
		cv2.waitKey(1)
		if i>=numPict:
			break
	cam.release()
	cv2.destroyAllWindows()
capture()
with open(directory+'/fichier.txt','w') as mon_fichier:
	# contex manager qui fermera le fichier à la fin du bloc with...
	mon_fichier.write("id= {} ,numPict= {}".format(id,i))
os.system("pause")
