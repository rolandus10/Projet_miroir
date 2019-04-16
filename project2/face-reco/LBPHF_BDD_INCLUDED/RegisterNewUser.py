
import os
import cv2
import numpy as np
from PIL import Image
import time
import mysql.connector #MAXIME
import time #MAXIME

def connection():
    print("CONNEXION A LA BDD EN COURS")
    db = mysql.connector.connect(host="localhost",user="HiReflect",password="pi=3.14", database="Students") #MAXIME
    #db = mysql.connector.connect(host="109.88.81.100",user="AlexisSANCHEZ",password="pi=3.14JOSEsanchez", database="Students") #MAXIME
    cursor = db.cursor() #MAXIME
    print("BDD CONNECTEE")
    return db,cursor
def who_are_you():
    """fonction qui récupère l'id d'une perssonne inconnue"""
    id = input('Entrez votre matricule : ')
    return id

def get_info(directory, id):
    """on retoutne le nombre de photos d'un individu + 20 (car on va en prendre 20 de plus)"""
    req="SELECT COUNT(*) FROM Picture WHERE studentId=%(studentId)s;"
    values={"studentId" : id}

    cursor.execute(req,values)
    rows=cursor.fetchall()

    for row in rows:
        i=row[0]
    numPict = i + 20
    return numPict

def capture(numPict, directory, faceDetec, id):
    """fonction qui prend les photos d'une personne, les convertis en noir et blanc et les recadres pour ne garder que le visage."""
    directory = directory + "/" +""+ str(id)
    cam = cv2.VideoCapture(0)
    i=0
    while (True):
        ret, img = cam.read();
        if not img is None:
            if not ret:
                cam = cv2.VideoCapture(0)
                continue
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceDetec.detectMultiScale(
                        img,
                        scaleFactor=1.2,
                        minNeighbors=7,
                        minSize=(50, 50)
                    )
            hMax=0
            wHMax=0
            xHMax=0
            yHMax=0
            for (x, y, w, h) in faces:
                if h>hMax:
                    hMax=h
                    wHMax=w
                    xHMax=x
                    yHMax=y
            i += 1
            # on enregistre l'image dans le fichier dataSet sous le nom User.id.i.jpg
            # gray[y:y+h,x:x+w] est l'image croppée on ne sauve que le visage.
            link=str(time.time()) + ".jpg"
            cv2.imwrite(directory+"_"+link, gray[yHMax:yHMax + hMax, xHMax:xHMax + wHMax])
            #on met toutes les photos dans le même dossier car c'est comme ca qu'on fait quand on a un serveur
            #on peut pas créer des sous-dossiers à chaque fois
        else:
            cam = cv2.VideoCapture(0)
#-------------------------------------------------------------------------------------------------------
            
            req='INSERT INTO Picture(pictureStorage,studentId) VALUES (%(pictureStorage)s,%(studentId)s)'
            values={"pictureStorage" : link, "studentId" : id}
            cursor.execute(req,values)
            db.commit()


#-------------------------------------------------------------------------------------------------------
            #pour la version d'essai ok mais pas pour le miroir définitif.
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # l'affichage est nécessaire pour la version d'essai mais avec le miroir on pourra l'enlever
        cv2.imshow("Face", img);
        # on attend 50 milli secondes pour pouvoir changer de tête grimace, profil, avec lunettes,...
        cv2.waitKey(50)
        if i >= numPict:
            break
    cam.release()
    cv2.destroyAllWindows()
    return i

def ouvrirImg(imdirectory):
    """ouvre une image et la convertit en numpy array"""
    faceImg = Image.open(imdirectory).convert('L')
    faceNp = np.array(faceImg, 'uint8')
    return faceNp

def trainer(directory):
    """ retourne une liste des images n'ayant pas encore étés utilisées pour entrainer le classifieur et une liste d'id correspondant aux photos dans le cas où on n'a pas encore un 'faceRecognizer'. """
    faces = []
    IDs = []
    req = "SELECT pictureStorage, studentId, pictureId from Picture"

    cursor.execute(req)
    rows = cursor.fetchall()

    for row in rows:
        imdirectory = directory + "/" + str(row[1])+"_"+str(row[0])
        faces.append(ouvrirImg(imdirectory))
        IDs.append(row[1])
        req2="UPDATE Picture SET trained = %(trained)s WHERE pictureId=%(pictureId)s"
        values = {"trained": 1, "pictureId": row[2]}
        cursor.execute(req2, values)
        db.commit()
    return np.array(IDs), faces

def retrainer(directory):
    """ retourne une liste des images n'ayant pas encore étés utilisées pour entrainer le classifieur et une liste d'id correspondant aux photos dans le cas où on a déjà un 'faceRecognizer'."""
    faces = []
    IDs = []
    req = "SELECT pictureStorage, studentId, pictureId FROM Picture WHERE trained=%(trained)s"
    values={"trained" : 0}

    cursor.execute(req)
    rows = cursor.fetchall()

    for row in rows:
        imdirectory = directory + "/" + str(row[1])+"_"+str(row[0])+".jpg"
        faces.append(ouvrirImg(imdirectory))
        IDs.append(row[1])
        req2="UPDATE Picture SET trained = %(trained) WHERE pictureId=%(pictureId)s"
        values = {"trained": 1, pictureId: row[3]}
        cursor.execute(req2, values)
        db.commit()
    return np.array(IDs), faces

def training(directory):
    """Crée et entraine le classifieur pour la première fois si le classifieur n'est pas trouvé. Ou entraine le classifieur s'il existe déjà"""
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

directory = "dataSet_LBPHF"
db,cursor=connection()
id=who_are_you()
faceDetec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
numPict=get_info(directory, id)
capture(numPict, directory, faceDetec, id)
training(directory)
