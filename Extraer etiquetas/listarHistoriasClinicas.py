# -*- coding: utf-8 -*-
"""
Created on Mon May  2 12:42:07 2022

@author: jm.rivera@uniandes.edu.co
"""

import os
import pandas as pd
import csv
import random
import docx2txt

def buscarPorId(id):
    data_raw.loc[data_raw['Historia Clínica'] == id]
    
def convertirATxt(direccion):
    nombreArchivo=direccion.split('/')[-1:][0]
    nuevoNombre=baseTxt+direccion.split('/')[-2:-1][0].split(' ')[1]+'/'+nombreArchivo.split('.')[0]+".txt"
    texto=docx2txt.process(direccion)
    
    f = open(nuevoNombre, "w+")
    f.write(texto)
    f.close()
    
def cargarBaseDeDatos():
    
    archivoEnExcel = 'D:/jmriv/Documents/Datos análisis de marcha/2022.xls'
    data_raw=pd.read_excel(archivoEnExcel)
    return data_raw

cirugia=[]
direccion=[]
palabrasPresentes=[]




# Importaremo la base de datos
base='D:/Users/USER/OneDrive - Universidad de los Andes/2022-1/Machine Learning/Proyecto/Datos/'
baseTxt='D:/Users/USER/OneDrive - Universidad de los Andes/2022-1/Machine Learning/Proyecto/DatosTxt/'

data_raw=cargarBaseDeDatos()
id=data_raw['Historia Clínica'].unique()


# Lista de carpetas en las que se buscarán las historias clínicas
carpetas=[]
for i in os.listdir(base):
    temp=base + '/'+i
    if os.path.isdir(temp) and i[0]!='.':
        carpetas.append(i)

direccionesAnalisis=[]
idAnalisis=[]
direccionesErrores=[]
numArchAnalisis=0
for i in carpetas:
    archivos=os.listdir(base+"/"+i)
    for j in archivos: 
        temp=base + i+"/"+j
        posibleId=j.split(" ")[0]
        try: 
            if int(posibleId) in id:
                numArchAnalisis+=1
                direccionesAnalisis.append(temp)
                idAnalisis.append(posibleId)
                
                
                newName=base+i+"/"+posibleId+temp[temp.find('.'):]
                if os.path.exists(newName):
                    newName=base+i+"/"+posibleId+"_"+str(numArchAnalisis)+temp[temp.find('.'):]
                os.rename(temp, newName)
            else:
                os.rename(temp, base + i+"/"+"zzz"+j)
                    
        except:
            #print("Error en el archivo "+temp)
            direccionesErrores.append(temp)
            
def convertirVariosArchivos(base, carpetas):
    for i in carpetas:
        archivos=os.listdir(base+"/"+i)
        for j in archivos:

            if j.split(".")[-1] == "docx":
                temp=base + i+"/"+j
                try:
                    convertirATxt(temp)
                except:
                    print(temp)
    
with open('fileList.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    #for i in direccionesAnalisis:
    writer.writerow(direccionesAnalisis)
    
with open('fileError.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    #for i in direccionesErrores:
    writer.writerow(direccionesErrores)
    

#print(os.listdir(base+"/"+carpetas[0])[7].split(" ")[0])
#print(data_raw['Historia Clínica'])
#print(os.listdir(base+"/"+carpetas[0])[7].split(" ")[0] in data_raw['Historia Clínica'])

historiasClinicasFaltantes=[]
for i in id:
    if str(i) in idAnalisis:
        a=1
    else: 
        historiasClinicasFaltantes.append(i)
    
#segundaBusqueda=[]        
#for i in historiasClinicasFaltantes:
#    temp = glob.glob(base + "/**/"+str(i)+"*", recursive = True)
#    segundaBusqueda.append(temp)