import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ⚡ Estilo CSS para pantalla completa
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

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Ventas",
    page_icon=":bar_chart:",
    layout="wide"
)

# Título y subtítulo
st.title("Análisis de Ventas 📊 - Productos Destacados")
st.subheader("Explora y visualiza las ventas de diferentes categorías y líneas de productos")

# Cargar datos
productos = pd.read_csv("data/Dim_Producto.csv", sep=",", quotechar='"')
ventas = pd.read_csv("data/Fact_Ventas.csv", sep=",", quotechar='"')

df = ventas.merge(productos, on="ID_Producto")

# Calculo de Margen_Realista_Ajustado
def calcular_margen(df):
    rand = np.random.randint(-5, 11, size=len(df)) / 100
    margenes_base = []
    for i in range(len(df)):
        prob = np.random.randint(1, 101)
        if prob <= 90:
            margen = 0.20 + rand[i]
        else:
            margen = 0.35 if np.random.randint(1, 3) == 1 else 0.05
        margenes_base.append(margen)
    df["Margen_Realista_Ajustado"] = df["Total_Ventas"] * margenes_base
    return df

df = calcular_margen(df)

# Layout principal: 3 columnas
col1, col2, col3 = st.columns([3, 3, 2])

with col1:
    # Fila 1: Segmentador
    categorias = df["Nombre_Categoria"].unique()
    filtro_categoria = st.multiselect("Filtra por categoría", categorias, default=categorias)

    df_filtrado = df[df["Nombre_Categoria"].isin(filtro_categoria)]

    # Fila 2: Gráfico de barras apiladas
    st.subheader("📊 Ventas por Línea y Categoría")
    agrupado = df_filtrado.groupby(["Nombre_Linea", "Nombre_Categoria"], as_index=False).sum()
    fig_bar = px.bar(
        agrupado,
        x="Total_Ventas",
        y="Nombre_Linea",
        color="Nombre_Categoria",
        orientation="h"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    # Fila 1: Gráfico de dispersión
    st.subheader("📈 Rentabilidad vs Volumen de Ventas")
    fig_disp = px.scatter(
        df_filtrado,
        x="Cantidad_Vendida",
        y="Margen_Realista_Ajustado",
        color="Nombre_Categoria",
        hover_data=["Nombre_Producto"]
    )
    st.plotly_chart(fig_disp, use_container_width=True)

    # Fila 2: Producto seleccionado
    st.subheader("🔎 Producto seleccionado")
    producto_sel = st.selectbox("Selecciona un producto:", df_filtrado["Nombre_Producto"].unique())
    st.write(df_filtrado[df_filtrado["Nombre_Producto"] == producto_sel])

with col3:
    # Fila 1: Tabla ordenada
    st.subheader("📋 Tabla de Datos")
    df_tabla = df_filtrado[[
        "Nombre_Producto", 
        "Margen_Realista_Ajustado", 
        "Cantidad_Vendida", 
        "Total_Ventas"
    ]]

    df_tabla = df_tabla.sort_values(
        by=["Cantidad_Vendida", "Total_Ventas", "Margen_Realista_Ajustado"],
        ascending=[False, False, False]
    )

    st.dataframe(df_tabla, use_container_width=True)

    # Fila 2: Totales dinámicos
    st.markdown("### 🔢 Totales dinámicos")
    total_margen = df_filtrado["Margen_Realista_Ajustado"].sum()
    total_cant = df_filtrado["Cantidad_Vendida"].sum()
    total_ventas = df_filtrado["Total_Ventas"].sum()

    st.write(f"**Total Margen Realista Ajustado:** ${total_margen:,.2f}")
    st.write(f"**Total Cantidad Vendida:** {total_cant:,}")
    st.write(f"**Total Ventas:** ${total_ventas:,.2f}")
