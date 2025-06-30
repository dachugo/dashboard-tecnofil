import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Rendimientos Comerciales",
    page_icon="〽️",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 1rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 1rem;
        max-width: 100% !important;
    }
    .st-emotion-cache-1w723zb, .st-emotion-cache-13ln4jf {
        max-width: 100% !important;
        width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("SECCIÓN: Rendimiento Comercial 〽️")
st.subheader("1. Evalúa el desempeño de sucursales y vendedores para mejorar la eficiencia comercial.")

fact_ventas = pd.read_csv("data/Fact_Ventas.csv", sep=",", quotechar='"')
dim_vendedor = pd.read_csv("data/Dim_Vendedor.csv", sep=",", quotechar='"')
dim_sucursal = pd.read_csv("data/Dim_Sucursal.csv", sep=",", quotechar='"')

# Merge
df = fact_ventas.merge(dim_vendedor, on="ID_Vendedor", how="left")
df = df.merge(dim_sucursal, on="ID_Sucursal", how="left")


zonas = sorted(df["Zona_Venta"].dropna().unique()) 

if "zonas_seleccionadas" not in st.session_state:
    st.session_state["zonas_seleccionadas"] = zonas.copy()

col_btn1, col_btn2 = st.columns([1, 1])
with col_btn1:
    if st.button("Seleccionar todas las zonas"):
        st.session_state["zonas_seleccionadas"] = zonas.copy()

with col_btn2:
    if st.button("Deseleccionar todas"):
        st.session_state["zonas_seleccionadas"] = []

# Multiselect controlado por el estado
zona_sel = st.multiselect(
    "Filtra por Zona de Venta:",
    options=zonas,
    default=st.session_state["zonas_seleccionadas"],
    key="zonas_seleccionadas"
)

df_filtrado = df[df["Zona_Venta"].isin(zona_sel)]

st.subheader("2. Resumen de Ventas por Vendedor")
tabla_vendedor = (
    df_filtrado.groupby("Nombre_x", as_index=False)[["Total_Ventas", "Cantidad_Vendida"]].sum()
    .sort_values(by="Total_Ventas", ascending=False)
)

st.dataframe(tabla_vendedor, use_container_width=True)

st.subheader("3. Ventas por Sucursal")
tabla_sucursal = df_filtrado.groupby(["Nombre_Sucursal", "Zona_Venta"], as_index=False)["Total_Ventas"].sum()
fig = px.bar(
    tabla_sucursal,
    x="Total_Ventas",
    y="Nombre_Sucursal",
    color="Zona_Venta",
    orientation="h",
    labels={
        "Total_Ventas": "Total Ventas",
        "Nombre_Sucursal": "Sucursal",
        "Zona_Venta": "Zona de Venta"
    },
    title="Total de Ventas por Sucursal y Zona"
)

st.plotly_chart(fig, use_container_width=True)
