import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title='Dashboard de Ventas', layout='wide')

# Título
st.title('Dashboard de Ventas — Superstore')

# Cargar datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv('Sample - Superstore.csv', encoding='latin1')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month
    return df

df = cargar_datos()

# Filtros en el sidebar
st.sidebar.header('Filtros')

# Filtro por año
años = sorted(df['Year'].unique())
año_seleccionado = st.sidebar.selectbox('Año', ['Todos'] + list(años))

# Filtro por región
regiones = sorted(df['Region'].unique())
region_seleccionada = st.sidebar.multiselect('Región', regiones, default=regiones)

# Filtro por categoría
categorias = sorted(df['Category'].unique())
categoria_seleccionada = st.sidebar.multiselect('Categoría', categorias, default=categorias)

# Aplicar filtros
if año_seleccionado != 'Todos':
    df = df[df['Year'] == año_seleccionado]

df = df[df['Region'].isin(region_seleccionada)]
df = df[df['Category'].isin(categoria_seleccionada)]

# Métricas principales
col1, col2, col3 = st.columns(3)
col1.metric('Ventas Totales', f"${df['Sales'].sum():,.0f}")
col2.metric('Ganancia Total', f"${df['Profit'].sum():,.0f}")
col3.metric('Número de Órdenes', f"{df.shape[0]:,}")

st.divider()

# Gráficos fila 1
col1, col2 = st.columns(2)
# Tabla de datos interactiva
st.divider()
st.subheader('Datos detallados')

# Mostrar tabla con columnas relevantes
columnas = ['Order Date', 'Region', 'Category', 'Sub-Category', 'Sales', 'Profit', 'Quantity']
st.dataframe(
    df[columnas].sort_values('Sales', ascending=False),
    use_container_width=True,
    height=400
)

# Botón para descargar los datos filtrados como CSV
csv = df[columnas].to_csv(index=False).encode('utf-8')
st.download_button(
    label='Descargar datos filtrados',
    data=csv,
    file_name='datos_filtrados.csv',
    mime='text/csv'
)

