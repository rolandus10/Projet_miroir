import os
import cv2
import numpy as np
from PIL import Image

recognizer= cv2.face.createLBPHFaceRecognizer()
path='dataSet_LBPHF'
def getImages_And_ID (path):
	''' crée une liste avec les chemin relatif des différentes images '''
	imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
	faces=[]
	IDs=[]
	for dirs in os.listdir(path):
		with open(path+'/'+dirs+'/fichier.txt','r') as mon_fichier:
			#contex manager qui fermera le fichier à la fin du bloc with...
			contenu=mon_fichier.read()
			pos1=contenu.find(',numPict= ')
			i=int(contenu[pos1+len(',numPict= '):])
		with open(path+'/'+dirs+'/trained.txt','w') as mon_fichier:
			#contex manager qui fermera le fichier à la fin du bloc with...
			mon_fichier.write("id= {}, numPict= {}".format(dirs,i))
	for subdir, dirs, files in os.walk(path):
		
		for file in files:
			if file.endswith('.jpg'):
				imPath=os.path.join(subdir, file)
				# for imPath in imagePaths:
				#faceImg est une image au format PIL ==> on doit la convertir en numpy car cv2 ne travail qu'avec des format numpy
				faceImg=Image.open(imPath).convert('L')
				faceNp=np.array(faceImg,'uint8')
				id=int(os.path.split(imPath)[-1].split('.')[1])
				# on rempli les listes
				faces.append(faceNp)
				IDs.append(id)
				cv2.imshow("training",faceNp)
				cv2.waitKey(1)
	return np.array(IDs),faces
IDs,faces=getImages_And_ID(path)
recognizer.train(faces,IDs)
# le fichier recognizer doit exister!
recognizer.save('recognizer/trainingData_LBPHF.yml')
cv2.destroyAllWindows()
