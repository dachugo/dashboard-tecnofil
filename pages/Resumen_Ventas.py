import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Resumen de Ventas",
    page_icon=":credit_card:",
    layout="wide"
)

st.title("SECCIÓN: Resumen de Ventas 💳")
st.subheader("1. Consulta las unidades y montos vendidos según el método de pago")

# Cargar datos
fact_ventas = pd.read_csv("data/Fact_Ventas.csv", sep=",", quotechar='"')
metodo_pago = pd.read_csv("data/Dim_MetodoPago.csv", sep=",", quotechar='"')
dim_tiempo = pd.read_csv("data/Dim_Tiempo.csv", sep=",", quotechar='"')
dim_producto = pd.read_csv("data/Dim_Producto.csv", sep=",", quotechar='"')

# Merge
fact_ventas = fact_ventas.merge(
    metodo_pago,
    on="ID_Pago",
    how="left"
).merge(
    dim_tiempo,
    on="ID_Tiempo",
    how="left"
).merge(
    dim_producto,
    on="ID_Producto",
    how="left"
)

# Filtros
metodos = metodo_pago["Método"].unique()
categorias = dim_producto["Nombre_Categoria"].unique()

metodo_seleccionado = st.multiselect(
    "Filtra por método de pago:",
    metodos,
    default=metodos
)

categoria_seleccionada = st.multiselect(
    "Filtra por categoría:",
    categorias,
    default=categorias
)

# Filtrado dinamico
df_filtrado = fact_ventas[
    (fact_ventas["Método"].isin(metodo_seleccionado)) &
    (fact_ventas["Nombre_Categoria"].isin(categoria_seleccionada))
]

col1, col2 = st.columns(2)

with col1:
    cantidad_total = df_filtrado["Cantidad_Vendida"].sum()
    st.markdown(
        f"""
        <div style="padding: 2rem; border-radius: 10px; text-align: center;">
            <h2 style="color: #4CAF50;">{cantidad_total:,} unidades vendidas</h2>
            <p style="font-size: 1.2rem;">Filtros aplicados</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    total_ventas = df_filtrado["Total_Ventas"].sum()
    st.markdown(
        f"""
        <div style="padding: 2rem; border-radius: 10px; text-align: center;">
            <h2 style="color: #2196F3;">${total_ventas:,.2f} en ventas</h2>
            <p style="font-size: 1.2rem;">Filtros aplicados</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Tabla detalle
st.subheader("Tabla Detallada de ventas por método de pago y categoría")
st.dataframe(
    df_filtrado.groupby(["Método", "Nombre_Categoria"], as_index=False)[["Cantidad_Vendida", "Total_Ventas"]].sum(),
    use_container_width=True
)

st.subheader("2. Gráfico de líneas: Ventas por Mes")

df_linea = (
    df_filtrado.groupby("Mes", as_index=False)["Total_Ventas"].sum()
    .sort_values("Mes")
)

fig_line = px.line(
    df_linea,
    x="Mes",
    y="Total_Ventas",
    markers=True,
    labels={"Mes": "Mes", "Total_Ventas": "Total Ventas"},
    title="Total Ventas por Mes"
)

st.plotly_chart(fig_line, use_container_width=True)

st.subheader("3. Gráfico de barras apiladas: Ventas por Categoría y Método")

df_barras = df_filtrado.groupby(["Nombre_Categoria", "Método"], as_index=False)["Total_Ventas"].sum()

fig_bar = px.bar(
    df_barras,
    x="Total_Ventas",
    y="Nombre_Categoria",
    color="Método",
    orientation="h",
    title="Ventas por Categoría y Método de Pago"
)

st.plotly_chart(fig_bar, use_container_width=True)
