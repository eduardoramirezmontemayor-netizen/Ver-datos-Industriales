import streamlit as st
import pandas as pd
import pickle

# Cargar modelo
model = pickle.load(open('modelo.pkl', 'rb'))

st.title("🔧 Predicción de Fallos Industriales")

# Entrada de datos
temperatura = st.number_input("Temperatura del aire [K]")
torque = st.number_input("Torque aplicado [Nm]")
rotacion = st.number_input("Velocidad de rotación [rpm]")
desgaste = st.number_input("Desgaste de herramienta [%]")

# Crear DataFrame con entrada
input_data = pd.DataFrame({
    'Air temperature [K]': [temperatura],
    'Torque [Nm]': [torque],
    'Rotational speed [rpm]': [rotacion],
    'Tool wear [min]': [desgaste]
})

# Predicción
if st.button("Predecir tipo de fallo"):
    pred = model.predict(input_data)
    st.success(f"🔍 Tipo de fallo predicho: {pred[0]}")
