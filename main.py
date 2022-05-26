import streamlit as st
from joblib import load
import preproccess
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración básica de la página
st.set_page_config(
  page_title="Analalizis de marcha", layout="wide",
)

# Clases proporcionadas por el negocio
classes = {
    0: "no necesita cirugia",
    1: "si necesita cirugía",
}

tipoCirugia={
    1: "alargamiento del tendón de aquiles",
    2: "alargamiento de la fascia",
}
  

tipoParalisis=["Ataxica",	"Diskinetica","Espastica",	"Hipotonica","Mixta"]
categoriasSilver=["Negativo", "Leve", "Positivo", "No evaluable"]

# Al tener que realizar la conexión una vez, utilizamos el decorador para no hacer varios llamados a la vez
@st.experimental_singleton
def upload():
    models = {
    'knn_si_no':{
        "name":"knn_si_no",
        "model": None
        },
    'svm_cirugia':{
        "name":"svm_cirugia",
        "model": None
        },  
    'scaler':{
        "name":"scaler",
        "model": None
        }, 
    }
    for name, values in models.items():
        values["model"] = load(f"classifiers/{name}.joblib")

    return models


models = upload() # Cargamos nuestros modelos
edad = st.number_input('Edad')
tonoGemelos= st.number_input('Tono gastrocnemios')
dorsiflexion= st.number_input('Dorsiflexión (en grados)')
felxPlantar= st.number_input("Felxion Plantar Tobillo (en grados)")
# silverskfold=st.number_input("Silfverskiold")
silverskfold = st.selectbox(
     'Silverskiöld',
     categoriasSilver)
tipoPar = st.selectbox(
     'Indique el tipo de parálisis del paciente',
     tipoParalisis)


def predict(edad, tonoGemelos, dorsiflexion, felxPlantar, silverskfold, tipoPar):
    """
    Realiza la predicción del texto según los modelos seleccionados.
    Args:
        - txt. Texto a analizar.
        - selection. Selección de modelos a utilizar.
    """

    # Realizamos una gráfica mostrando los porcentajes de confianza de los modelos
    fig = make_subplots()
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')

    txt=preproccess.procesarInput(edad, tonoGemelos, dorsiflexion, felxPlantar, silverskfold, tipoPar, models['scaler']['model'])
    print(txt)

    p = models['knn_si_no']["model"].predict(txt)[0] # Obtenemos la clase del modelo según la predicción
    proba = models['knn_si_no']["model"].predict_proba(txt)[0] # Obtenemos las probabiidades de pertenencia de cada clase
    labelClase=classes[p]
    
    #st.markdown('La prediccón es que el paciente '+labelClase + " con una probabilidad del "+str(proba[0]*100)+"%") # Mostramos el resultado apra cada uno de los modelos seleccionados
    st.markdown('La prediccón es que el paciente '+labelClase) # Mostramos el resultado apra cada uno de los modelos seleccionados

    if p ==1:
        cirugia=models['svm_cirugia']['model'].predict(txt)[0]
        labelCirugia=tipoCirugia[cirugia]
        st.markdown('La cirugía predicha para este paciente es '+labelCirugia) # Mostramos el resultado apra cada uno de los modelos seleccionados

pred = st.button("Predecir") # Botón para predecir
if pred:
    predict(edad, tonoGemelos, dorsiflexion, felxPlantar, silverskfold, tipoPar)