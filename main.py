import streamlit as st

st.set_page_config(
  page_title="Laboratorio 2", layout="wide",
)

from joblib import load
from preproccess import TextPreprocessing
import plotly.graph_objects as go
from plotly.subplots import make_subplots

classes = {
    1: "Neoplasms.",
    2: "Digestive System Diseases.",
    3: "Nervous System Diseases.",
    4: "Cardiovascular Diseases.",
    5: "General Pathological Conditions."
}

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

models = upload()
selection = st.multiselect("Models",models.keys(), list(models.keys())[0],format_func=lambda x: models.get(x)['name'])

def predict(txt,selection):
    fig = make_subplots()
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')

    for m in selection:
        p = models[m]["model"].predict([txt])[0]
        proba = models[m]["model"].predict_proba([txt])[0]
        st.markdown(f'For **{models[m]["name"]}**, the class predicted is *{classes[p]}*')

        fig.add_trace(
            go.Bar(
                x=list(classes.values()),
                y=proba,
                name=models[m]["name"]
            ))

    fig.update_yaxes(range=[0,1])
    fig.update_xaxes(title_text="Classes")
    st.plotly_chart(fig,use_container_width=True)

txt = st.text_area("Medical Abstract", value="",height = 400)
pred = st.button("Predict")
if pred:
    predict(txt, selection)