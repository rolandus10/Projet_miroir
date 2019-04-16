def ouvrirImg(imdirectory):
    faceImg = Image.open(imdirectory).convert('L')
    faceNp = np.array(faceImg, 'uint8')
    return faceNp

def retrainer(directory):
    """ crée une liste avec les chemin relatif des différentes images """
    faces = []
    IDs = []
    req = "SELECT pictureStorage, studentId, trained, pictureId from Picture"

    cursor.execute(req)
    rows = cursor.fetchall()

    for row in rows:
        if int(row[2])==0:
            imdirectory = directory + "/" + str(row[1])+"_"+str(row[0])+".jpg"
            faces.append(ouvrirImg(imdirectory))
            IDs.append(row[1])
            req2="UPDATE Picture SET trained = %(trained) WHERE pictureId=%(pictureId)s"
            values = {"trained": 1, pictureId: row[3]}
            cursor.execute(req, values)
    return np.array(IDs), faces
def trainer(directory):
    """ crée une liste avec les chemin relatif des différentes images """
    faces = []
    IDs = []
    req = "SELECT pictureStorage, studentId, pictureId from Picture"

    cursor.execute(req)
    rows = cursor.fetchall()

    for row in rows:
        imdirectory = directory + "/" + str(row[1])+"_"+str(row[0])+".jpg"
        faces.append(ouvrirImg(imdirectory))
        IDs.append(row[1])
        req2="UPDATE Picture SET trained = %(trained) WHERE pictureId=%(pictureId)s"
        values = {"trained": 1, pictureId: row[2]}
        cursor.execute(req, values)
    return np.array(IDs), faces