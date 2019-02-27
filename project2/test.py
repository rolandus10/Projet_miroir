def fct():
    compt=0
    while compt<4:
        x=input("x = \n")
        try:
            x=int(x)
            return x
        except:
            compt+=1
            if compt>=4:
                return 1
            print(compt)
fct()
            
