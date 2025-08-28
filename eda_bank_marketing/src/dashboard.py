#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard Interactivo para Análisis de Marketing Bancario
Autor: Bernardo Novelo Rotger
Fecha: 28/08/2025
Descripción: Aplicación web interactiva para explorar resultados del EDA
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Marketing Bancario",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("Dashboard de Análisis de Marketing Bancario")
st.markdown("---")

# Cargar datos
@st.cache_data
def load_data():
    """Carga los datos procesados"""
    try:
        # Cargar dataset unificado
        merged_df = pd.read_csv('data/processed/bank_customers_merged.csv')
        return merged_df
    except:
        st.error("❌ Error al cargar los datos. Asegúrate de ejecutar el análisis primero.")
        return None

# Cargar datos
df = load_data()

if df is not None:
    # Sidebar para filtros
    st.sidebar.header("Filtros")
    
    # Filtro por canal de contacto
    contact_options = ['Todos'] + list(df['contact'].unique())
    selected_contact = st.sidebar.selectbox("Canal de Contacto", contact_options)
    
    # Filtro por rango de edad
    age_range = st.sidebar.slider("Rango de Edad", 
                                 int(df['age'].min()), 
                                 int(df['age'].max()), 
                                 (int(df['age'].min()), int(df['age'].max())))
    
    # Aplicar filtros
    if selected_contact != 'Todos':
        filtered_df = df[(df['contact'] == selected_contact) & 
                        (df['age'] >= age_range[0]) & 
                        (df['age'] <= age_range[1])]
    else:
        filtered_df = df[(df['age'] >= age_range[0]) & 
                        (df['age'] <= age_range[1])]
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_contacts = len(filtered_df)
        st.metric("Total Contactos", f"{total_contacts:,}")
    
    with col2:
        conversion_rate = filtered_df['y'].mean() * 100
        st.metric("Tasa Conversión", f"{conversion_rate:.2f}%")
    
    with col3:
        avg_age = filtered_df['age'].mean()
        st.metric("Edad Promedio", f"{avg_age:.1f} años")
    
    with col4:
        avg_campaign = filtered_df['campaign'].mean()
        st.metric("Promedio Campaña", f"{avg_campaign:.1f} contactos")
    
    st.markdown("---")
    
    # Gráficos interactivos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribución de Edad")
        fig_age = px.histogram(filtered_df, x='age', nbins=30, 
                              title="Distribución de Edad de Clientes",
                              color_discrete_sequence=['#1f77b4'])
        fig_age.update_layout(showlegend=False)
        st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        st.subheader("Conversión por Canal")
        conversion_by_contact = filtered_df.groupby('contact')['y'].agg(['mean', 'count']).reset_index()
        fig_contact = px.bar(conversion_by_contact, x='contact', y='mean',
                            title="Tasa de Conversión por Canal",
                            color_discrete_sequence=['#ff7f0e'])
        fig_contact.update_layout(yaxis_title="Tasa de Conversión")
        st.plotly_chart(fig_contact, use_container_width=True)
    
    # Análisis de correlación
    st.subheader("Matriz de Correlación")
    numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
    correlation_matrix = filtered_df[numeric_cols].corr()
    
    fig_corr = px.imshow(correlation_matrix,
                         title="Matriz de Correlación de Variables Numéricas",
                         color_continuous_scale='RdBu',
                         aspect="auto")
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Análisis por ocupación
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Conversión por Ocupación")
        conversion_by_job = filtered_df.groupby('job')['y'].agg(['mean', 'count']).reset_index()
        conversion_by_job = conversion_by_job[conversion_by_job['count'] >= 100]  # Filtrar por frecuencia
        conversion_by_job = conversion_by_job.sort_values('mean', ascending=False)
        
        fig_job = px.bar(conversion_by_job.head(10), x='job', y='mean',
                         title="Top 10 Ocupaciones por Tasa de Conversión",
                         color_discrete_sequence=['#2ca02c'])
        fig_job.update_layout(xaxis_tickangle=-45, yaxis_title="Tasa de Conversión")
        st.plotly_chart(fig_job, use_container_width=True)
    
    with col2:
        st.subheader("Conversión vs Número de Contactos")
        conversion_by_campaign = filtered_df.groupby('campaign')['y'].agg(['mean', 'count']).reset_index()
        conversion_by_campaign = conversion_by_campaign[conversion_by_campaign['count'] >= 5]
        
        fig_campaign = px.scatter(conversion_by_campaign, x='campaign', y='mean', 
                                 size='count', title="Conversión vs Contactos",
                                 color_discrete_sequence=['#d62728'])
        fig_campaign.update_layout(xaxis_title="Número de Contactos", 
                                 yaxis_title="Tasa de Conversión")
        st.plotly_chart(fig_campaign, use_container_width=True)
    
    # Análisis temporal
    st.subheader("Análisis Temporal")
    
    if 'contact_month' in filtered_df.columns:
        monthly_conversion = filtered_df.groupby('contact_month')['y'].mean().reset_index()
        fig_monthly = px.line(monthly_conversion, x='contact_month', y='y',
                             title="Tasa de Conversión por Mes",
                             color_discrete_sequence=['#9467bd'])
        fig_monthly.update_layout(yaxis_title="Tasa de Conversión")
        st.plotly_chart(fig_monthly, use_container_width=True)
    
    # Tabla de datos filtrados
    st.subheader("Datos Filtrados")
    st.dataframe(filtered_df.head(100), use_container_width=True)
    
    # Descarga de datos filtrados
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Descargar Datos Filtrados (CSV)",
        data=csv,
        file_name=f'marketing_bancario_filtrado_{selected_contact}_{age_range[0]}-{age_range[1]}.csv',
        mime='text/csv'
    )

else:
    st.error("""
    ## Datos no encontrados
    
    Para usar este dashboard, primero debes ejecutar el análisis:
    
    ```bash
    cd src
    python eda.py
    ```
    
    O instalar Streamlit y ejecutar:
    
    ```bash
    pip install streamlit
    streamlit run src/dashboard.py
    ```
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Dashboard creado con Streamlit | Análisis de Marketing Bancario | ThePowerMBA</p>
</div>
""", unsafe_allow_html=True) 