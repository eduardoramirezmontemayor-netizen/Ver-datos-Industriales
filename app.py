import streamlit as st
import pandas as pd
import pickle

# Cargar el modelo entrenado
with open('modelo.pkl', 'rb') as f:
    model = pickle.load(f)

# Configuración de la página
st.set_page_config(page_title="Predicción de Fallos Industriales", layout="centered")
st.title("🔧 Predicción de Fallos Industriales")
st.markdown("Introduce los parámetros operativos para predecir el tipo de fallo.")

# Entradas del usuario
temperatura_aire = st.number_input("Temperatura del aire [K]", min_value=250.0, max_value=400.0, value=300.0)
temperatura_proceso = st.number_input("Temperatura del proceso [K]", min_value=250.0, max_value=400.0, value=310.0)
rotacion = st.number_input("Velocidad de rotación [rpm]", min_value=0.0, max_value=5000.0, value=1500.0)
torque = st.number_input("Torque aplicado [Nm]", min_value=0.0, max_value=100.0, value=40.0)
desgaste = st.number_input("Desgaste de herramienta [min]", min_value=0.0, max_value=300.0, value=50.0)

# Selección del tipo de producto
tipo = st.selectbox("Tipo de producto", ["M", "L"])

# Codificación manual de variables dummy
type_L = 1 if tipo == "L" else 0
type_M = 1 if tipo == "M" else 0

# Construcción del DataFrame con las entradas del usuario
input_data = pd.DataFrame({
    'Air temperature [K]': [temperatura_aire],
    'Process temperature [K]': [temperatura_proceso],
    'Rotational speed [rpm]': [rotacion],
    'Torque [Nm]': [torque],
    'Tool wear [min]': [desgaste],
    'Type_L': [type_L],
    'Type_M': [type_M]
})

# Columnas esperadas por el modelo (sin 'Target')
expected_columns = ['Air temperature [K]', 'Process temperature [K]',
                    'Rotational speed [rpm]', 'Torque [Nm]',
                    'Tool wear [min]', 'Type_L', 'Type_M']

# Añadir columnas faltantes con valor neutro
for col in expected_columns:
    if col not in input_data.columns:
        input_data[col] = 0

# Reordenar columnas y asegurar tipo numérico
input_data = input_data[expected_columns].astype(float)

# Predicción
if st.button("Predecir tipo de fallo"):
    try:
        pred = model.predict(input_data)
        st.success(f"🔍 Tipo de fallo predicho: {pred[0]}")
    except Exception as e:
        st.error("❌ Error al realizar la predicción. Verifica los datos de entrada.")
