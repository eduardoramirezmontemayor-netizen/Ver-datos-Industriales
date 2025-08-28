import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# Cargar el modelo entrenado
with open('modelo.pkl', 'rb') as f:
    model = pickle.load(f)

# Obtener columnas esperadas directamente del modelo
expected_columns = model.feature_names_in_.tolist()

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
type_L = 1 if tipo == "L" else 0
type_M = 1 if tipo == "M" else 0

# Construcción del DataFrame
input_data = pd.DataFrame({
    'Air temperature [K]': [temperatura_aire],
    'Process temperature [K]': [temperatura_proceso],
    'Rotational speed [rpm]': [rotacion],
    'Torque [Nm]': [torque],
    'Tool wear [min]': [desgaste],
    'Type_L': [type_L],
    'Type_M': [type_M]
})

# Diagnóstico visual
st.subheader("🔍 Diagnóstico de entrada")
st.write("Columnas esperadas por el modelo:")
st.write(expected_columns)
st.write("Columnas enviadas desde la app:")
st.write(input_data.columns.tolist())

# Predicción
if st.button("Predecir tipo de fallo"):
    try:
        # Adaptar columnas
        for col in expected_columns:
            if col not in input_data.columns:
                input_data[col] = 0
        input_data = input_data[expected_columns].astype(float)

        # Predicción
        pred = model.predict(input_data)[0]
        st.success(f"🔍 Tipo de fallo predicho: {pred}")

        # Probabilidades
        proba = model.predict_proba(input_data)[0]
        classes = model.classes_
        proba_df = pd.DataFrame({
            'Tipo de fallo': classes,
            'Probabilidad': proba
        }).sort_values(by='Probabilidad', ascending=False)

        # Alerta preventiva si hay riesgo significativo
        fallo_total = 1 - proba_df[proba_df['Tipo de fallo'] == 'No Failure']['Probabilidad'].values[0]
        if fallo_total > 0.2:
            st.warning(f"⚠️ Riesgo detectado: {fallo_total:.2%} de probabilidad acumulada de fallo. Revisión recomendada.")

        # Mostrar tabla
        st.subheader("📊 Probabilidades por tipo de fallo")
        st.dataframe(proba_df.style.format({'Probabilidad': '{:.2%}'}))

        # Gráfico de barras
        st.subheader("📈 Visualización de probabilidades")
        fig, ax = plt.subplots()
        ax.barh(proba_df['Tipo de fallo'], proba_df['Probabilidad'], color='steelblue')
        ax.set_xlabel("Probabilidad")
        ax.invert_yaxis()
        st.pyplot(fig)

    except Exception as e:
        st.error("❌ Error al realizar la predicción. Verifica que todos los datos estén completos y en el formato correcto.")
