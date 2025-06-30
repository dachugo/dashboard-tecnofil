import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Optimización Inventarios",
    page_icon="📦",
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
    </style>
    """,
    unsafe_allow_html=True
)

st.title("SECCIÓN: Optimización de Inventarios 📦")
st.subheader("Detectar ineficiencias en el stock para reducir desperdicios y mejorar la sostenibilidad.")

# Cargar datos
fact_ventas = pd.read_csv("data/Fact_Ventas.csv", sep=",", quotechar='"')
dim_producto = pd.read_csv("data/Dim_Producto.csv", sep=",", quotechar='"')
dim_sucursal = pd.read_csv("data/Dim_Sucursal.csv", sep=",", quotechar='"')

# Merge
df = fact_ventas.merge(dim_producto, on="ID_Producto", how="left")
df = df.merge(dim_sucursal, on="ID_Sucursal", how="left")

# Selector de sucursal
sucursales = sorted(df["Nombre"].dropna().unique())
if "sucursales_sel" not in st.session_state:
    st.session_state["sucursales_sel"] = sucursales.copy()

col_btn1, col_btn2 = st.columns([1, 1])
with col_btn1:
    if st.button("Seleccionar todas las sucursales"):
        st.session_state["sucursales_sel"] = sucursales.copy()

with col_btn2:
    if st.button("Deseleccionar todas"):
        st.session_state["sucursales_sel"] = []

sucursal_sel = st.multiselect(
    "Filtra por Sucursal:",
    options=sucursales,
    default=st.session_state["sucursales_sel"],
    key="sucursales_sel"
)

# Filtrado
df_filtrado = df[df["Nombre"].isin(sucursal_sel)]

# Grafico de barras apiladas
st.subheader("1. Stock por Categoría de Producto")
tabla_categoria = (
    df_filtrado.groupby(["Nombre_Categoria", "Nombre"], as_index=False)["Stock"].sum()
)

fig = px.bar(
    tabla_categoria,
    x="Stock",
    y="Nombre_Categoria",
    color="Nombre",
    orientation="h",
    labels={
        "Stock": "Stock Disponible",
        "Nombre_Categoria": "Categoría",
        "Nombre_Sucursal": "Sucursal"
    },
    title="Stock disponible por Categoría y Sucursal"
)

st.plotly_chart(fig, use_container_width=True)

# Tabla detalle
st.subheader("2. Detalle de Inventario y Ventas")
tabla_detalle = df_filtrado.groupby(
    ["Nombre_Producto"],
    as_index=False
)[["Cantidad_Vendida", "Stock"]].sum().sort_values(by="Cantidad_Vendida", ascending=False)

st.dataframe(tabla_detalle, use_container_width=True)
