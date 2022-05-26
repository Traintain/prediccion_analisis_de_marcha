import contractions
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from sklearn.preprocessing import StandardScaler

from sklearn.base import BaseEstimator,TransformerMixin
import pandas as pd

def procesarInput(edad, tono, dorsi, flexi, silvers, tipo, scaler):
    atax,disk,espas,hipo,mix=0,0,0,0,0

    if tipo == "Ataxica":
        atax=1
    elif tipo == "Diskinetica":
        disk=1
    elif tipo == "Espastica":
        espas=1
    elif tipo == "Hipotonica":
        hipo=1
    else:
        mix=1

    if silvers == "Negativo":
        silvers=0
    elif silvers == "Leve":
        silvers=1
    elif silvers == "Positivo":
        silvers=2
    elif silvers == "No evaluable":
        silvers=3

    example={"Edad":[edad],"Tono gastrocnemios":[ tono ], "Dorsiflexion":[dorsi], "Felxion Plantar Tobillo":[flexi],
    "Silfverskiold":[silvers],"Ataxica":[atax],"Diskinetica":[disk],"Espastica":[espas],"Hipotonica":[hipo],"Mixta":[mix]}
    # Se convierte el diccionario a dataframe
    entrada=pd.DataFrame.from_dict(example)
    
    columns = ['Edad', 'Tono gastrocnemios', 'Dorsiflexion', 'Felxion Plantar Tobillo','Silfverskiold']
    data_norm=entrada[columns]
    print(data_norm)
    data_norm = scaler.transform(data_norm)
    print(data_norm)
    data_norm = pd.DataFrame(data_norm,columns=columns)
    data_norm[['Ataxica', 'Diskinetica','Espastica', 'Hipotonica', 'Mixta']]=entrada[['Ataxica', 'Diskinetica',
       'Espastica', 'Hipotonica', 'Mixta']]

    return data_norm
