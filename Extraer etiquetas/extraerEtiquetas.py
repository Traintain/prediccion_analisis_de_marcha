# -*- coding: utf-8 -*-
"""
Created on Fri May  6 19:31:23 2022

@author: jmriv
"""
import os
import pandas as pd
import string

unificarTerminos={
    "facia":"fascia",
    "fasia":"fascia",
    "gastrognemio":"gemelo",
    "gastrocnemio":"gemelo",
    "sóleo":"soleo",
    "bauman":"baumman",
    "baumann":"baumman",
    "baummann":"baumman",
    "bowman":"baumman",
    "bawman":"baumman",
    "liberación":"liberacion",
    "tendón":"tendon",
    "fasciotomía":"fasciotomia",
    "faciotomía":"fasciotomia",
    "fasiotomía":"fasciotomia",
    "de":"",
    "el":"",
    "la":"",
    "los":"",
    "las":"",
    "del":"",
    "y":"",
    "para":"",
    "una":"",
    "uno":"",
    "con":"",
    }


palabrasCirugia=["liberacion",
                 "alarga",
                 "strayer",
                 "baker",
                 "bauman",
                 "vulpius",
                 "hoke",
                 "fasciotom"]

palabras=["liberacion posterior",
                 "alargamiento tendon aquiles",
                 "alargamiento zalargamiento fascia",
                 "alargar la fascia",
                 "zalargamiento",
                 "gastrognemio",
                 "gastrocnemio",
                 "gemelo",
                 "soleo",
                 "strayer",
                 "baker",
                 "bauman",
                 "vulpius",
                 "hoke"]


def buscarEnBD():
    baseTxt='D:/Users/USER/OneDrive - Universidad de los Andes/2022-1/Machine Learning/Proyecto/DatosTxt/'
    for i in os.listdir(baseTxt):
        buscarEnCarpeta(i)
    
    

def buscarEnCarpeta(i):
    #base='D:/Users/USER/OneDrive - Universidad de los Andes/2022-1/Machine Learning/Proyecto/Datos'
    base='D:/Users/USER/OneDrive - Universidad de los Andes/2022-1/Machine Learning/Proyecto/DatosTxt'
    #base="C:/Users/jmriv/Desktop/Historias clinicas preguntar Mafe/"
    
    archivos=os.listdir(base+"/"+i)
    
    nomArchivos=[]
    derecho=[]
    izquierdo=[]
    frases=[]
    
    for j in archivos:
        dere,izq,frase=buscarEnArchivo(base+"/"+i+"/"+j)
        nomArchivos.append(j)
        derecho.append(dere)
        izquierdo.append(izq)
        frases.append(frase)
    
    data={"archvios":archivos, "etiqueta derecha":derecho, "etiqueta izquierda": izquierdo, "frases":frases}
    pd.DataFrame.from_dict(data).to_excel(str(i)+".xlsx")
        
def buscarEnArchivo(direccion):
    
    claseDerecho=0
    claseIzquierdo=0
    
    try: 
        with open(direccion, encoding="utf8") as f:
            lineas=f.readlines()
            #Leeremos cada historia clínica línea por línea
            lineaAnterior=""
            frases=[]
            for i in lineas:
                if lineaAnterior == "":
                    lineaAnterior=i
                else:
                    newLine=i+lineaAnterior
                    claseDerecho, claseIzquierdo, temp = buscarEnFrase(newLine, claseDerecho, claseIzquierdo)
                    if len(temp)>0:
                        frases.append(temp)
    except:
        #print(direccion)
        with open(direccion) as f:
            lineas=f.readlines()
            #Leeremos cada historia clínica línea por línea
            lineaAnterior=""
            frases=[]
            for i in lineas:
                if lineaAnterior == "":
                    lineaAnterior=i
                else:
                    newLine=i+lineaAnterior
                    claseDerecho, claseIzquierdo, temp = buscarEnFrase(newLine, claseDerecho, claseIzquierdo)
                    if len(temp)>0:
                        frases.append(temp)
    #print(claseDerecho)
    return claseDerecho, claseIzquierdo, frases

def buscarEnFrase(newLine, cD, cI):
    frases=[]
    claseDerecho=cD
    claseIzquierdo=cI
    
    # Quitamos las mayúsculas de la línea
    newLine=to_lowercase(newLine)
    # Quitaremos palabras de interés que tengan tildes y conectores
    newLine=reemplazarPalabras(newLine)

    # Vamos a mirar si alguna de las raices de interés está presente
    for k in palabrasCirugia:
        pointer=newLine.find(k)
        
        # Si está presente, vamos a ver por cada caso si dice el 
        # tipo de cirugía y el lado al que se quiere realizar
        if pointer != -1:
            frase=newLine[pointer:]
            # Miramos si luego de "liberación" dice "posterior"
            if k == "liberacion":
                if frase.find("liberacion posterior")!=-1:
                    claseDerecho, claseIzquierdo = revisarLado(newLine, 1, claseDerecho, claseIzquierdo)
                    #print(k)
                    #print(claseDerecho, claseIzquierdo)
                    frases.append(newLine)
            
            # Miramos si luego de "alargamiento" dice "fascia o gemelos"
            elif k=="alarga":
                if frase.find("fascia")!=-1 or frase.find("gemelo")!=-1:
                    # print("fasci gemelo")
                    claseDerecho, claseIzquierdo = revisarLado(newLine, 2, claseDerecho, claseIzquierdo)
                    frases.append(newLine)
                    
                # Miramos si luego de "alargamiento" hay una "z" sin letras alrededor o un "zalargamiento"
                elif newLine.find("zalargamiento")!=-1:
                    claseDerecho, claseIzquierdo = revisarLado(newLine, 1, claseDerecho, claseIzquierdo)
                    frases.append(newLine)
                elif frase.find("z")!=-1:
                    if frase[ frase.find("z")-1 ] not in string.ascii_letters and frase[ frase.find("z")+1 ] not in string.ascii_letters:
                        claseDerecho, claseIzquierdo = revisarLado(newLine, 1, claseDerecho, claseIzquierdo)
                        frases.append(newLine)
            elif k=="strayer" or k == "baker" or k == "bauman":
                claseDerecho, claseIzquierdo = revisarLado(newLine, 2, claseDerecho, claseIzquierdo)                    
                frases.append(newLine)
                
            elif k=="vulpius":
                claseDerecho, claseIzquierdo = revisarLado(newLine, 1, claseDerecho, claseIzquierdo)
                frases.append(newLine)
            
            elif k=="fasciotom":
                #print(k)
                if frase.find("gemelo")!=-1:
                    claseDerecho, claseIzquierdo = revisarLado(newLine, 2, claseDerecho, claseIzquierdo)
                    frases.append(newLine)
    # print(newLine)
    return claseDerecho,claseIzquierdo, frases

def revisarLado(newLine,clase, cD, cI):
    claseDerecho=cD
    claseIzquierdo=cI
    
    if newLine.find("derech")!=-1:
        if cD==0 or cD==clase:
            claseDerecho=clase
        else:
            claseDerecho=-1
    elif newLine.find("izquie")!=-1:
        if cI==0 or cI==clase:
            claseIzquierdo=clase
        else:
            claseIzquierdo=-1
    elif newLine.find("gemelos")!=-1:
        if (cI==0 and cD==0) or (cI==clase and cD==clase):
            claseDerecho=clase
            claseIzquierdo=clase
        else:
            claseDerecho=-1
            claseIzquierdo=-1  
    elif newLine.find("bilateral")!=-1:
        if (cI==0 and cD==0) or (cI==clase and cD==clase):
            claseDerecho=clase
            claseIzquierdo=clase
        else:
            claseDerecho=-1
            claseIzquierdo=-1  
    else:
        claseDerecho=-1
        claseIzquierdo=-1
    #print(claseDerecho)
    #print(claseIzquierdo)
    return claseDerecho, claseIzquierdo    
             
def to_lowercase(phrase):
    new_phrase = []
    for letter in phrase:
        new_letter = letter.lower()
        new_phrase.append(new_letter)
    return "".join(new_phrase)

def reemplazarPalabras(frase):
    palabras=frase.split(" ")
    for j in range(len(palabras)):
        if unificarTerminos.get(palabras[j]) != None:
            palabras[j]=unificarTerminos.get(palabras[j])+" "
        else:
            palabras[j]=palabras[j]+" "
    return "".join(palabras)
