import os
import cv2
import numpy as np
from PIL import Image
recognizer= cv2.face.createLBPHFaceRecognizer()
recognizer.load("recognizer\\trainingData_LBPHF.yml")
path='dataSet_LBPHF'
# il faut créer un fichier avec l'id et le numéro de la dernière photo
# print(os.listdir(path))
def getImages_And_ID (path):
	''' crée une liste avec les chemin relatif des différentes images '''
	# pour un gain de temps et plus de facilité il faut créer un fichier par id dès le début.
	imagePaths=[]
	for f in os.listdir(path):
		directory=path+'/'+f
		with open(directory+'/trained.txt','r') as mon_fichier:
			contenu=mon_fichier.read()
			pos1=contenu.find(', numPict= ')
			numPicFinal=int(contenu[pos1+len(', numPict= '):])
			pos1=contenu.find('id= ')
			pos2=contenu.find(', numPict= ')
			idAdd=int(contenu[pos1+len('id= '):pos2])
			# print('id= {}, numPict= {}'.format(idAdd,numPicFinal))
		with open(directory+'/fichier.txt','r') as mon_fichier:
			#contex manager qui fermera le fichier à la fin du bloc with...
			contenu=mon_fichier.read()
			pos1=contenu.find(',numPict= ')
			i=int(contenu[pos1+len(',numPict= '):])
		if i!=numPicFinal:
			for fi in os.listdir(directory):
				if fi.endswith('.jpg'):
					pos1=fi.find('.'+str(idAdd)+'.') 
					pos2=fi.find('.jpg')
					numPic=int(fi[pos1+len('.'+str(idAdd)+'.'):pos2])
					if numPic>numPicFinal:
						# print(fi[pos1+len('.'+str(idAdd)+'.'):pos2])
						newF=fi
						imagePaths.append(os.path.join(directory,fi))
				with open(directory+'/trained.txt','w') as mon_fichier:
					mon_fichier.write("id= {}, numPict= {}".format(idAdd,i))
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
		# pas obligatoire --> gain de temps si on n'affiche pas 
		cv2.imshow("training",faceNp)
		cv2.waitKey(1)
	return np.array(IDs),faces
IDs,faces=getImages_And_ID (path)
recognizer.update(faces,IDs)
# le fichier recognizer doit exister!
recognizer.save('recognizer/trainingData_LBPHF.yml')
cv2.destroyAllWindows()
os.system("pause")
