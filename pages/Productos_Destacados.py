import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Productos Destacados",
    page_icon="🎁",
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

st.title("SECCIÓN: Productos Destacados 🎁")
st.subheader("1. Explora y visualiza las ventas de diferentes categorías y líneas de productos")


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

# Cargar datos
productos = pd.read_csv("data/Dim_Producto.csv", sep=",", quotechar='"')
ventas = pd.read_csv("data/Fact_Ventas.csv", sep=",", quotechar='"')
df = ventas.merge(productos, on="ID_Producto")

# Calcular margen ANTES de usarlo
df = calcular_margen(df)

# Ahora ya tiene Margen_Realista_Ajustado
categorias = df["Nombre_Categoria"].unique()
filtro_categoria = st.multiselect("Filtra por categoría", categorias, default=categorias)
df_filtrado = df[df["Nombre_Categoria"].isin(filtro_categoria)]

# Ahora puedes calcular totales
total_margen = df_filtrado["Margen_Realista_Ajustado"].sum()
total_cant = df_filtrado["Cantidad_Vendida"].sum()
total_ventas = df_filtrado["Total_Ventas"].sum()

# Mostrar totales
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("**Total Margen Realista Ajustado:**")
    st.markdown(
        f"<h2 style='color:#4CAF50;'>{total_margen:,.2f}</h2>",
        unsafe_allow_html=True
    )

with col_b:
    st.markdown("**Total Cantidad Vendida:**")
    st.markdown(
        f"<h2 style='color:#FF9800;'>{total_cant:,}</h2>",
        unsafe_allow_html=True
    )

with col_c:
    st.markdown("**Total Ventas:**")
    st.markdown(
        f"<h2 style='color:#2196F3;'>${total_ventas:,.2f}</h2>",
        unsafe_allow_html=True
    )

df = calcular_margen(df)

col1, col2, col3 = st.columns([3, 3, 2])
with col1:
    st.subheader("2. Ventas por Línea y Categoría")
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
    st.subheader("3. Rentabilidad vs Volumen de Ventas")
    fig_disp = px.scatter(
        df_filtrado,
        x="Cantidad_Vendida",
        y="Margen_Realista_Ajustado",
        color="Nombre_Categoria",
        hover_data=["Nombre_Producto"]
    )
    st.plotly_chart(fig_disp, use_container_width=True)

    st.subheader("Producto seleccionado")
    producto_sel = st.selectbox("Selecciona un producto:", df_filtrado["Nombre_Producto"].unique())
    st.write(df_filtrado[df_filtrado["Nombre_Producto"] == producto_sel])

with col3:
    st.subheader("4. Tabla de Datos")
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

    st.data_editor(
        df_tabla,
        column_config={
            "Nombre_Producto": st.column_config.TextColumn(width="small"),
            "Margen_Realista_Ajustado": st.column_config.NumberColumn(width="small"),
            "Cantidad_Vendida": st.column_config.NumberColumn(width="small"),
            "Total_Ventas": st.column_config.NumberColumn(width="small"),
        },
        use_container_width=True,
        disabled=True
    )



