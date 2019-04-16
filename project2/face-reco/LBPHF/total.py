import os
import cv2
import numpy as np
from PIL import Image
import time

def menu():
    print('nouvel utilisateur      --> 1')
    print('entrainer le recognizer --> 2')
    print('reconnaissance faciale  --> 3')
    print('quitter le programme    --> 4')
    choix = int(input(''))
    return choix

# fct pour la création de data
def who_are_you():
    id = input('enter user id\n')
    return id

# on fait un fichier par personne
def get_info(directory, id):
    directory = directory + "/" + str(id)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if os.path.isfile(directory + '/fichier.txt'):
        with open(directory + '/fichier.txt', 'r') as mon_fichier:
            contenu = mon_fichier.read()
        pos1 = contenu.find(',numPict= ')
        i = int(contenu[pos1 + len(',numPict= '):])
        numPict = i + 20
    else:
        numPict = 20
        i = 0
    return numPict, i

def capture(i, numPict, directory, faceDetec, id):
    directory = directory + "/" + str(id)
    cam = cv2.VideoCapture(0)
    while (True):
        ret, img = cam.read();
        if not ret: continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetec.detectMultiScale(gray, 1.4, 5)
        for (x, y, w, h) in faces:
            i += 1
            # on enregistre l'image dans le fichier dataSet sous le nom User.id.i.jpg
            # gray[y:y+h,x:x+w] est l'image croppée on ne sauve que le visage.
            cv2.imwrite(directory + "/User." + str(id) + "." + str(i) + ".jpg", gray[y:y + h, x:x + w])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # on attend 150 milli secondes pour pouvoir changer de tête grimace, profil, avec lunettes,...
            cv2.waitKey(150)
        # l'affichage est nécessaire pour la version d'essai mais avec le miroir on pourra l'enlever
        cv2.imshow("Face", img);
        cv2.waitKey(1)
        if i >= numPict:
            break
    cam.release()
    cv2.destroyAllWindows()
    return i

def save_info(directory, id, i):
    directory = directory + "/" + str(id)
    with open(directory + '/fichier.txt', 'w') as mon_fichier:
        mon_fichier.write("id= {} ,numPict= {}".format(id, i))

# -------------------------------------------------------------------------------------------------------------------------------------------
# les deux fonctions qui suivent servent à aller chercher les images et les id's correspondants dans les fichiers
# la première prend toutes les photos et la seconde sélectionne les photos qui n'ont pas encore été utilisées par l'algo
def trainer(directory):
    """ crée une liste avec les chemin relatif des différentes images """
    imagedirectorys = [os.path.join(directory, f) for f in os.listdir(directory)]
    faces = []
    IDs = []
    # on parcours tous les utilisateurs
    for dirs in os.listdir(directory):
        with open(directory + '/' + dirs + '/fichier.txt', 'r') as mon_fichier:
            contenu = mon_fichier.read()
            pos1 = contenu.find(',numPict= ')
            i = int(contenu[pos1 + len(',numPict= '):])
        with open(directory + '/' + dirs + '/trained.txt', 'w') as mon_fichier:
            mon_fichier.write("id= {}, numPict= {}".format(dirs, i))
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.jpg'):
                imdirectory = os.path.join(subdir, file)
                # faceImg est une image au format PIL ==> on doit la convertir en tableau(numpy array) car cv2 ne travail qu'avec des format numpy
                faceImg = Image.open(imdirectory).convert('L')
                faceNp = np.array(faceImg, 'uint8')
                id = int(os.path.split(imdirectory)[-1].split('.')[1])
                faces.append(faceNp)
                IDs.append(id)
    return np.array(IDs), faces

def retrainer(directory):
    """ crée une liste avec les chemin relatif des différentes images """
    imagedirectorys = []
    dir = directory
    for f in os.listdir(directory):
        directory = dir + '/' + f
        if not os.path.exists(directory + '/trained.txt'):
            with open(directory + '/trained.txt', 'w') as mon_fichier:
                mon_fichier.write("id= {}, numPict= {}".format(f, 0))
        with open(directory + '/trained.txt', 'r') as mon_fichier:
            contenu = mon_fichier.read()
        pos1 = contenu.find(', numPict= ')
        numPicFinal = int(contenu[pos1 + len(', numPict= '):])
        pos1 = contenu.find('id= ')
        pos2 = contenu.find(', numPict= ')
        idAdd = int(contenu[pos1 + len('id= '):pos2])
        with open(directory + '/fichier.txt', 'r') as mon_fichier:
            contenu = mon_fichier.read()
        pos1 = contenu.find(',numPict= ')
        i = int(contenu[pos1 + len(',numPict= '):])
        if i != numPicFinal:
            for fi in os.listdir(directory):
                if fi.endswith('.jpg'):
                    pos1 = fi.find('.' + str(idAdd) + '.')
                    pos2 = fi.find('.jpg')
                    numPic = int(fi[pos1 + len('.' + str(idAdd) + '.'):pos2])
                    if numPic > numPicFinal:
                        imagedirectorys.append(os.path.join(directory, fi))
            with open(directory + '/trained.txt', 'w') as mon_fichier:
                mon_fichier.write("id= {}, numPict= {}".format(idAdd, i))
    faces = []
    IDs = []
    for imdirectory in imagedirectorys:
        faceImg = Image.open(imdirectory).convert('L')
        faceNp = np.array(faceImg, 'uint8')
        id = int(os.path.split(imdirectory)[-1].split('.')[1])
        faces.append(faceNp)
        IDs.append(id)
    return np.array(IDs), faces

# -------------------------------------------------------------------------------------------------------------------------------------------
def reco(faceDetec):
    recognizer = cv2.face.createLBPHFaceRecognizer()
    recognizer.load("recognizer/trainingData_LBPHF.yml")
    id = 0
    it = 0
    dist = 0
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_COMPLEX
    # la reco ne marchera pas s'il y a plusieurs personnes sur l'image.
    # prendre les rectangle ayant la plus grde largeur seulement.
    while it < 20:
        ret, img = cam.read();
        # parfois la webcam ne renvoie rien comme première image ce qui produit une erreur
        if not ret: continue
        cv2.imshow("Face", img);
        cv2.waitKey(1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetec.detectMultiScale(
	        img,
	        scaleFactor=1.2,
	        minNeighbors=7,
	        minSize=(50, 50)
            )
        for (x, y, w, h) in faces:
            collector = cv2.face.StandardCollector_create()
            recognizer.predict_collect(gray[y:y + h, x:x + w], collector)
            if collector.getMinDist()<75:
                it += 1
                dist = dist + collector.getMinDist()
                id = collector.getMinLabel()
                # avec cette méthode, si la dernière prédiction est mauvaise, on sort avec le mauvais nom ...
                # a remplacer par des requète sql ds la base de données
                # créer un dictionnaire avec comme clé l'id et comme contenu une sorte d'itérateur puis à la fin, on prend l'id avec le plus grand iérateur...
                if id == 1:
                    id = "Alexis"
                elif id == 2:
                    id = "Santo"
                elif id == 3:
                    id = "Maxime M"
                elif id == 4:
                    id = "Julie"
                elif id == 5:
                    id = "Anouar"
                elif id == 6:
                    id = "Maxime H"
                elif id == 7:
                    id = "Aurelie <3"
                elif id==12:
                    id="Carine"
                print("{}".format(id))
    cam.release()
    cv2.destroyAllWindows()
    return id, dist, it

def training(directory):
    debut = time.time()
    recognizer = cv2.face.createLBPHFaceRecognizer()
    if os.path.exists("recognizer/trainingData_LBPHF.yml"):
        IDs, faces = retrainer(directory)
        recognizer.load("recognizer/trainingData_LBPHF.yml")
        recognizer.update(faces, IDs)
    else:
        IDs, faces = trainer(directory)
        recognizer.train(faces, IDs)
    recognizer.save('recognizer/trainingData_LBPHF.yml')
    fin = time.time()
    print("{}".format(fin - debut))

def createData(directory):
    faceDetec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    if not os.path.exists(directory):
        os.makedirs(directory)
    id = who_are_you()
    numPict, i = get_info(directory, id)
    i = capture(i, numPict, directory, faceDetec, id)
    save_info(directory, id, i)
    training(directory)

def facialReco(directory):
    faceDetec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    id, dist, it = reco(faceDetec)
    if dist / it < 50:  # 100 = dist max (c'est bcp en moy qd il reconnait bien on est à 60-70) avec 100 photos je descend jusqu'à 30-35
        print("distance moyenne de l\'essai courant = {}\nBonjour {}".format(dist / it, id))
    else:
        print("je ne suis pas sûr de vous reconnaître ... êtes vous {}".format(id))
        x = input('oui/non')
        if x.upper() == 'NON':
            print('je vais vous enregistrer')
            createData(directory)
        # ----------------- stats perso à enlever pour la fin
    with open('fichier.txt', 'a') as mon_fichier:
        mon_fichier.write("{}\n".format(dist / it))
    dist_moy = 0
    i = 0
    with open('fichier.txt', 'r') as mon_fichier:
        for ligne in mon_fichier.readlines():
            ligne = ligne[0:len(ligne) - len("\n")]
            dist_moy += float(ligne)
            i += 1
    dist_moy = dist_moy / i
    print("distance moyenne globale (fichier.txt){}".format(dist_moy))

# ----------------------------------------------------------------------------------------------------
print('Hi reflect vous salue :-)')
directory = "dataSet_LBPHF"
facialReco(directory)
