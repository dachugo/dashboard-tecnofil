import streamlit as st

st.set_page_config(
    page_title="Dashboard de Ventas",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title("Dashboard de Ventas 🚀")

# Mostrar imagen del dashboard
st.image("screenshots/screenshot_1 (1).jpeg", caption="Vista principal del Dashboard de Ventas", use_column_width=True)

st.write("Usa el menú lateral para navegar entre las secciones del análisis.")