import os
import cv2
import numpy as np
from PIL import Image

recognizer= cv2.face.LBPHFaceRecognizer_create()
path='dataSet'
def getImages_And_ID (path):
	''' crée une liste avec les chemin relatif des différentes images '''
	imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
	faces=[]
	IDs=[]
	for imPath in imagePaths:
		#faceImg est une image au format PIL ==> on doit la convertir en numpy car cv2 ne travail qu'avec des format numpy
		faceImg=Image.open(imPath).convert('L')
		faceNp=np.array(faceImg,'uint8')
		id=int(os.path.split(imPath)[-1].split('.')[1])
		# on rempli les listes 
		faces.append(faceNp)
		IDs.append(id)
		cv2.imshow("training",faceNp)
		cv2.waitKey(10)
	return np.array(IDs),faces
IDs,faces=getImages_And_ID (path)
recognizer.train(faces,IDs)
# le fichier recognizer doit exister!
recognizer.save('recognizer/trainingData.yml')
cv2.destroyAllWindows()
os.system("pause")
