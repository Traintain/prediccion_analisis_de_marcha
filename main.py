import streamlit as st
from joblib import load
from preproccess import TextPreprocessing
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración básica de la página
st.set_page_config(
  page_title="Laboratorio 2", layout="wide",
)

# Clases proporcionadas por el negocio
classes = {
    1: "Neoplasms.",
    2: "Digestive System Diseases.",
    3: "Nervous System Diseases.",
    4: "Cardiovascular Diseases.",
    5: "General Pathological Conditions."
}

# Al tener que realizar la conexión una vez, utilizamos el decorador para no hacer varios llamados a la vez
@st.experimental_singleton
def upload():
    models = {
    'grid_search_NB':{
        "name":"Multinomial Bayes",
        "model": None
        },
    'grid_search_pre':{
        "name":"Ensemblers (Precision)",
        "model": None
        },
    'grid_search_knn':{
        "name":"K-Nearest Neighbors",
        "model": None
        },     
    }
    for name, values in models.items():
        values["model"] = load(f"classifiers/{name}.pkl")

    return models


models = upload() # Cargamos nuestros modelos
selection = st.multiselect("Models",models.keys(), list(models.keys())[0],format_func=lambda x: models.get(x)['name']) # Generamos una selección múltiple de nuestros modelos

def predict(txt,selection):
    """
    Realiza la predicción del texto según los modelos seleccionados.
    Args:
        - txt. Texto a analizar.
        - selection. Selección de modelos a utilizar.
    """

    # Realizamos una gráfica mostrando los porcentajes de confianza de los modelos
    fig = make_subplots()
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')

    for m in selection:
        p = models[m]["model"].predict([txt])[0] # Obtenemos la clase del modelo según la predicción
        proba = models[m]["model"].predict_proba([txt])[0] # Obtenemos las probabiidades de pertenencia de cada clase
        st.markdown(f'For **{models[m]["name"]}**, the class predicted is *{classes[p]}*') # Mostramos el resultado apra cada uno de los modelos seleccionados

        # Añadimos cada predicción según su probabilidad.
        fig.add_trace(
            go.Bar(
                x=list(classes.values()),
                y=proba,
                name=models[m]["name"]
            ))

    fig.update_yaxes(range=[0,1])
    fig.update_xaxes(title_text="Classes")
    st.plotly_chart(fig,use_container_width=True)

txt = st.text_area("Medical Abstract", value="",height = 400) # Mostramos el área donde se copia el texto
pred = st.button("Predict") # Botón para predecir
if pred:
    predict(txt, selection)