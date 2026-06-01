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
años = sorted(df['Year'].unique())
año_seleccionado = st.sidebar.selectbox('Año', ['Todos'] + list(años))
regiones = sorted(df['Region'].unique())
region_seleccionada = st.sidebar.multiselect('Región', regiones, default=regiones)
categorias = sorted(df['Category'].unique())
categoria_seleccionada = st.sidebar.multiselect('Categoría', categorias, default=categorias)

# Aplicar filtros
if año_seleccionado != 'Todos':
    df = df[df['Year'] == año_seleccionado]
df = df[df['Region'].isin(region_seleccionada)]
df = df[df['Category'].isin(categoria_seleccionada)]

# KPIs
st.subheader('Indicadores Clave')
col1, col2, col3, col4 = st.columns(4)
col1.metric('Ventas Totales', f"${df['Sales'].sum():,.0f}")
col2.metric('Ganancia Total', f"${df['Profit'].sum():,.0f}")
col3.metric('Margen de Ganancia', f"{(df['Profit'].sum() / df['Sales'].sum() * 100):.1f}%")
col4.metric('Ticket Promedio', f"${df['Sales'].mean():,.0f}")

st.divider()

# Fila 1 — Ventas por categoría y región
col1, col2 = st.columns(2)
with col1:
    ventas_categoria = df.groupby('Category')['Sales'].sum().reset_index()
    fig1 = px.bar(ventas_categoria, x='Category', y='Sales',
                  title='Ventas por Categoría', color='Category')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    ventas_region = df.groupby('Region')['Sales'].sum().reset_index()
    fig2 = px.bar(ventas_region, x='Region', y='Sales',
                  title='Ventas por Región', color='Region')
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Fila 2 — Mapa y dispersión
col1, col2 = st.columns(2)
with col1:
    ventas_estado = df.groupby('State')['Sales'].sum().reset_index()
    fig3 = px.choropleth(ventas_estado,
                         locations='State',
                         locationmode='USA-states',
                         color='Sales',
                         scope='usa',
                         title='Mapa de Ventas por Estado',
                         color_continuous_scale='Blues')
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    fig4 = px.scatter(df, x='Sales', y='Profit',
                      color='Category', size='Quantity',
                      title='Ventas vs Ganancia por Categoría',
                      hover_data=['Sub-Category'])
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# Fila 3 — Evolución anual y ganancia por categoría
col1, col2 = st.columns(2)
with col1:
    ventas_mes = df.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
    fig5 = px.line(ventas_mes, x='Month', y='Sales', color='Year',
                   title='Evolución Mensual de Ventas', markers=True)
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    ganancia_categoria = df.groupby('Category')['Profit'].sum().reset_index()
    fig6 = px.bar(ganancia_categoria, x='Category', y='Profit',
                  title='Ganancia por Categoría', color='Category')
    st.plotly_chart(fig6, use_container_width=True)

st.divider()

# Top 10 productos
st.subheader('Top 10 Productos más Vendidos')
top10 = df.groupby('Product Name')['Sales'].sum().reset_index()
top10 = top10.sort_values('Sales', ascending=False).head(10)
fig7 = px.bar(top10, x='Sales', y='Product Name',
              orientation='h', title='Top 10 Productos',
              color='Sales', color_continuous_scale='Blues')
fig7.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig7, use_container_width=True)

st.divider()

# Tabla de datos
st.subheader('Datos Detallados')
columnas = ['Order Date', 'Region', 'Category', 'Sub-Category', 'Sales', 'Profit', 'Quantity']
st.dataframe(df[columnas].sort_values('Sales', ascending=False),
             use_container_width=True, height=400)

csv = df[columnas].to_csv(index=False).encode('utf-8')
st.download_button(label='Descargar datos filtrados',
                   data=csv, file_name='datos_filtrados.csv', mime='text/csv')

