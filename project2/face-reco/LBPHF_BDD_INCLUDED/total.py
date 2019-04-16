import os
import cv2
import numpy as np
from PIL import Image
import time
import mysql.connector

def connection():
    print("CONNEXION A LA BDD EN COURS")
    db = mysql.connector.connect(host="localhost",user="HiReflect",password="pi=3.14", database="Students")
    #db = mysql.connector.connect(host="109.88.81.100",user="alexis",password="pi=314", database="Students")
    cursor = db.cursor()
    #print("BDD CONNECTEE")
    return db,cursor

def menu():
    print('nouvel utilisateur      --> 1')
    print('entrainer le recognizer --> 2')
    print('reconnaissance faciale  --> 3')
    print('quitter le programme    --> 4')
    choix = int(input(''))
    return choix

def who_are_you():
    """fonction qui récupère l'id d'une perssonne inconnue"""
    id = input('Entrez votre matricule chiffre par chiffre: ')
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
            link=str(time.time()) + ".jpg"
            cv2.imwrite(directory+"_"+link, gray[yHMax:yHMax + hMax, xHMax:xHMax + wHMax])
#-------------------------------------------------------------------------------------------------------
            
            req='INSERT INTO Picture(pictureStorage,studentId) VALUES (%(pictureStorage)s,%(studentId)s);'
            values={"pictureStorage" : link, "studentId" : id}
            cursor.execute(req,values)
            db.commit()
        else:
            cam = cv2.VideoCapture(0)


#-------------------------------------------------------------------------------------------------------
            #pour la version d'essai ok mais pas pour le miroir définitif.
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # l'affichage est nécessaire pour la version d'essai mais avec le miroir on pourra l'enlever
        cv2.imshow("Face", img);
        # on attend 15 milli secondes (pas trop longtemps car ça ralentit fortement le programme) pour pouvoir changer de tête: grimace, profil, avec lunettes,...
        cv2.waitKey(15)
        if i >= numPict:
            break
    cam.release()
    cv2.destroyAllWindows()

def ouvrirImg(imdirectory):
    """ouvre une image et la convertit en numpy array"""
    faceImg = Image.open(imdirectory).convert('L')
    faceNp = np.array(faceImg, 'uint8')
    return faceNp

def retrainer(directory):
    """ retourne une liste des images n'ayant pas encore étés utilisées pour entrainer le classifieur et une liste d'id correspondant aux photos dans le cas où on a déjà un 'faceRecognizer'."""
    faces = []
    IDs = []
    req = "SELECT pictureStorage, studentId, pictureId FROM Picture WHERE trained=%(trained)s;"
    values={"trained" : 0}

    cursor.execute(req,values)
    rows = cursor.fetchall()

    for row in rows:
        imdirectory = directory + "/" + str(row[1])+"_"+str(row[0])
        faces.append(ouvrirImg(imdirectory))
        IDs.append(row[1])
        req2="UPDATE Picture SET trained = %(trained)s WHERE pictureId=%(pictureId)s;"
        values = {"trained": 1, pictureId: row[3]}
        cursor.execute(req2, values)
        db.commit()
    return np.array(IDs), faces

def trainer(directory):
    """ retourne une liste des images n'ayant pas encore étés utilisées pour entrainer le classifieur et une liste d'id correspondant aux photos dans le cas où on n'a pas encore un 'faceRecognizer'. """
    faces = []
    IDs = []
    req = "SELECT pictureStorage, studentId, pictureId from Picture;"

    cursor.execute(req)
    rows = cursor.fetchall()

    for row in rows:
        imdirectory = directory + "/" + str(row[1])+"_"+str(row[0])
        faces.append(ouvrirImg(imdirectory))
        IDs.append(row[1])
        req2="UPDATE Picture SET trained = %(trained)s WHERE pictureId=%(pictureId)s;"
        values = {"trained": 1, "pictureId": row[2]}
        cursor.execute(req2, values)
        db.commit()
    return np.array(IDs), faces

def numberOfRec(id):
    req="SELECT numberOfRec FROM Student WHERE studentId=%(studentId)s;"
    values={"studentId" : id}
    cursor.execute(req,values)
    rows=cursor.fetchall()
    numRec=0
    for row in rows:
        numRec=row[0]
    numRec+=1
    req2="UPDATE Student SET numberOfRec = %(numberOfRec)s WHERE studentId=%(studentId)s;"
    values = {"numberOfRec": numRec, "studentId": id}
    cursor.execute(req2, values)
    db.commit()

def reco(faceDetec):
    """execute une boucle qui va tenter de reconnaître la personne face à la webcam. Retourne un id, une distance(estimation de la certitude de la reconnaissance) """
    recognizer = cv2.face.createLBPHFaceRecognizer()
    recognizer.load("recognizer/trainingData_LBPHF.yml")
    id = 0
    it = 0
    k=0
    dist = 0
    cam = cv2.VideoCapture(0)
    while it < 20:
        k+=1
        ret, img = cam.read();
        # parfois la webcam ne renvoie rien comme première image ce qui produit une erreur
        if not img is None:
            if not ret:
                cam = cv2.VideoCapture(0)
                continue
            #plus nécessaire dans la version finale
            cv2.imshow("Face", img);
            cv2.waitKey(1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceDetec.detectMultiScale(
                    img,
                    scaleFactor=1.2,
                    minNeighbors=7,
                    minSize=(50, 50)
                )
            #résolution du problème "si plusieur personne se mettent devant le miroir"
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
            if hMax>0:
                collector = cv2.face.StandardCollector_create()
                recognizer.predict_collect(gray[yHMax:yHMax + hMax, xHMax:xHMax + wHMax], collector)
                #pour que la reco soit plus fiable, on peut diminuer la tolérance minimale mais il faudra plus de temps pour reconnaître 20 fois une personne mais on ne peux pas descendre sous 50
                if collector.getMinDist()<85:
                    it += 1
                    dist = dist + collector.getMinDist()
                    id = collector.getMinLabel()
                    numberOfRec(id)
        else:
            cam = cv2.VideoCapture(0)
        if k>=100:
            break
    cam.release()
    cv2.destroyAllWindows()
    req="SELECT studentId FROM Student WHERE numberOfRec=(SELECT MAX(numberOfRec) FROM Student);"
    cursor.execute(req)
    rows = cursor.fetchall()
    for row in rows:
        id=row[0]
    req="UPDATE Student SET numberOfRec = %(numberOfRec)s;"
    values = {"numberOfRec": 0}
    cursor.execute(req, values)
    db.commit()
    return id, dist, it

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

def createData(directory):
    """On demande le matricule, on récupère les infos correspondantes à ce matricule, on prend 20 photos puis on réentraine le classifieur"""
    faceDetec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    if not os.path.exists(directory):
        os.makedirs(directory)
    id = who_are_you()
    numPict= get_info(directory, id)
    capture(numPict, directory, faceDetec, id)
    training(directory)

def facialReco(directory):
    faceDetec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    id, dist, it = reco(faceDetec)
    if it>0:
        if dist / it < 50:  # 50 = dist max (qd il reconnait bien on est à 60-70) avec 100 photos je descend jusqu'à 30-35
            print("distance moyenne de l\'essai courant = {}\nBonjour {}".format(dist / it, id))
        else:
            print("je ne suis pas sûr de vous reconnaître ... êtes vous {}".format(id))
            x = input('oui/non')
            if x.upper() == 'NON':
                print('je vais vous enregistrer')
                createData(directory)
    
# ----------------------------------------------------------------------------------------------------
print('Hi reflect vous salue :-)')
directory = "dataSet_LBPHF"
db,cursor=connection()
facialReco(directory)
