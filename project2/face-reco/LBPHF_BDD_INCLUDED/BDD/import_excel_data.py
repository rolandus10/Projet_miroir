import xlrd
import os
import re
import mysql.connector
import sys


db = mysql.connector.connect(host="localhost",user="HiReflect",password="pi=3.14", database="Students")
cursor = db.cursor()
    

#------------------------------------------------------------------------------


filesNames = os.listdir("./Excel_files")    #take excel files names

for fName in filesNames:

    #bug si on ouvre le fichier excel en meme temps qu'on lance le programme python
    print('\n\n-----------------'+fName+'------------------')

    pattern='[A-Za-z]{2,3}[0-9]{1}_{0,1}[A-Za-z]{0,10}'
    blocName=re.search(pattern,fName,flags=0)
    blocName=blocName.group(0)
    
    blocName=blocName.replace("_"," ")

    f=xlrd.open_workbook('./Excel_files/'+fName)

    data=list()
  
    for sheetName in f.sheet_names():
        sheet=f.sheet_by_name(sheetName)

        for rowNum in range(sheet.nrows):
            data.append(sheet.row_values(rowNum))  #add to list at each iteration

        cursor.execute("""SELECT blocId FROM Bloc WHERE blocTitle=%(blocTitle)s""",{"blocTitle" : blocName})
        rows=cursor.fetchall()
     
        if rows:

            for row in rows:
                blocId=row[0]

        else:
            raise Exception("Ce bloc n'existe pas")




    for d in data:
        #print(d)

        pattern='[0-9]{6}'
        i=0
        while i<len(d): #not a for because we need to access second element

            string=str(d[i])
            matricule = re.search(pattern, string, flags=0)

            if matricule:
                matricule=matricule.group(0)
                #faire une regex pour vérifier que nom et prénom sont bons et pas infos qui ont été intercalées
                nom=d[i+1]
                prenom=d[i+2]
                #print(prenom,nom,matricule)
        
                stud = {"studentId" : matricule, "surname": nom, "name" : prenom}
                stud2 = {"studentId" : matricule, "blocId": blocId}

               
                cursor.execute("""SELECT studentId FROM Student WHERE studentId=%s""",(matricule, ))
                rows=cursor.fetchall()

                if rows:    #student already registered
                    try:
                        cursor.execute("""UPDATE Student SET name=%(name)s,surname=%(surname)s WHERE studentId=%(studentId)s""",stud)
                        db.commit()
                    except:
                        print("La modification de "+matricule+" a échoué")

                    try:
                        cursor.execute("""INSERT INTO TakeBloc (studentId,blocId) VALUES(%(studentId)s,%(blocId)s""",stud2)
                        db.commit()
                    except:
                        pass #do nothing if already inserted in DB

                
                else:
                    try:
                        cursor.execute("""INSERT INTO Student (studentId, name, surname) VALUES(%(studentId)s, %(name)s, %(surname)s)""", stud)
                        cursor.execute("""INSERT INTO TakeBloc (studentId,blocId) VALUES(%(studentId)s,%(blocId)s""",stud2)
                        db.commit()
                                       
                    except:
                        print("L'insertion de "+matricule+" a échoué")
                        
                    
                break   #stop when we have found the informations of the row
            i+=1

db.close()
