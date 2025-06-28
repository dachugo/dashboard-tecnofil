import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

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

# Segmentador
categorias = df["Nombre_Categoria"].unique()
filtro_categoria = st.multiselect("Filtra por categoría", categorias, default=categorias)

df_filtrado = df[df["Nombre_Categoria"].isin(filtro_categoria)]

# Gráfico de barras apiladas
agrupado = df_filtrado.groupby(["Nombre_Linea", "Nombre_Categoria"], as_index=False).sum()

fig_bar = px.bar(
    agrupado,
    x="Total_Ventas",
    y="Nombre_Linea",
    color="Nombre_Categoria",
    orientation="h",
    title="Ventas por Línea y Categoría"
)
st.plotly_chart(fig_bar)

# Gráfico de dispersión
fig_disp = px.scatter(
    df_filtrado,
    x="Cantidad_Vendida",
    y="Margen_Realista_Ajustado",
    color="Nombre_Categoria",
    hover_data=["Nombre_Producto"],
    title="Rentabilidad vs Volumen de Ventas"
)
st.plotly_chart(fig_disp)

# Tabla
st.dataframe(df_filtrado[["Nombre_Producto", "Margen_Realista_Ajustado", "Cantidad_Vendida", "Total_Ventas"]], use_container_width=True)
