#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis Avanzado - Marketing Bancario
Autor: Bernardo Novelo Rotger
Fecha: 28/08/2025
Descripción: Análisis avanzado con segmentación y cohortes
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

def segmentar_clientes(df):
    """Segmenta clientes usando clustering"""
    print("Segmentando clientes...")
    
    # Seleccionar variables para segmentación
    segment_vars = ['age', 'campaign', 'duration', 'emp_var_rate', 'cons_price_idx']
    segment_df = df[segment_vars].dropna()
    
    # Estandarizar variables
    scaler = StandardScaler()
    segment_scaled = scaler.fit_transform(segment_df)
    
    # Aplicar PCA para reducción de dimensionalidad
    pca = PCA(n_components=3)
    segment_pca = pca.fit_transform(segment_scaled)
    
    # Clustering con K-means
    kmeans = KMeans(n_clusters=4, random_state=42)
    clusters = kmeans.fit_predict(segment_pca)
    
    # Añadir clusters al dataframe
    segment_df['cluster'] = clusters
    
    # Análisis de clusters
    cluster_analysis = segment_df.groupby('cluster').agg({
        'age': ['mean', 'count'],
        'campaign': 'mean',
        'duration': 'mean',
        'emp_var_rate': 'mean'
    }).round(2)
    
    print("Segmentación completada")
    print("\n📊 Análisis de Clusters:")
    print(cluster_analysis)
    
    return segment_df, clusters

def analisis_cohortes(df):
    """Análisis de cohortes temporales"""
    print("\nAnalizando cohortes temporales...")
    
    if 'contact_month' in df.columns:
        # Crear cohortes por mes
        monthly_cohorts = df.groupby('contact_month')['y'].agg(['mean', 'count']).reset_index()
        
        # Análisis de tendencias
        print("Tendencias mensuales de conversión:")
        print(monthly_cohorts.sort_values('contact_month'))
        
        # Visualización de cohortes
        plt.figure(figsize=(12, 6))
        plt.plot(monthly_cohorts['contact_month'], monthly_cohorts['mean'], 
                marker='o', linewidth=2, markersize=8)
        plt.title('Tasa de Conversión por Mes', fontsize=16, fontweight='bold')
        plt.xlabel('Mes', fontsize=12)
        plt.ylabel('Tasa de Conversión', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('../figures/cohortes_temporales.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("Gráfico de cohortes guardado")
        
        return monthly_cohorts
    
    return None

def analisis_roi_campanas(df):
    """Análisis de ROI por campaña"""
    print("\nAnalizando ROI de campañas...")
    
    # Simular costos (en un caso real vendrían de datos externos)
    cost_per_contact = 2.5  # Euros por contacto
    
    # Calcular métricas por campaña
    campaign_roi = df.groupby('campaign').agg({
        'y': ['mean', 'count'],
        'duration': 'mean'
    }).round(4)
    
    campaign_roi.columns = ['conversion_rate', 'total_contacts', 'avg_duration']
    
    # Calcular costos y ROI
    campaign_roi['total_cost'] = campaign_roi['total_contacts'] * cost_per_contact
    campaign_roi['conversions'] = campaign_roi['total_contacts'] * campaign_roi['conversion_rate']
    
    # Valor promedio por conversión (simulado)
    avg_conversion_value = 500  # Euros
    campaign_roi['total_revenue'] = campaign_roi['conversions'] * avg_conversion_value
    campaign_roi['roi'] = (campaign_roi['total_revenue'] - campaign_roi['total_cost']) / campaign_roi['total_cost']
    
    print("ROI por Número de Contactos:")
    print(campaign_roi.round(4))
    
    # Identificar campañas más rentables
    profitable_campaigns = campaign_roi[campaign_roi['roi'] > 0]
    print(f"\nCampañas Rentables (ROI > 0): {len(profitable_campaigns)}")
    
    return campaign_roi

def analisis_estacionalidad(df):
    """Análisis de patrones estacionales"""
    print("\nAnalizando patrones estacionales...")
    
    if 'contact_month' in df.columns:
        # Análisis por mes
        monthly_patterns = df.groupby('contact_month').agg({
            'y': 'mean',
            'campaign': 'mean',
            'duration': 'mean'
        }).round(4)
        
        print("Patrones Mensuales:")
        print(monthly_patterns)
        
        # Identificar mejores y peores meses
        best_month = monthly_patterns['y'].idxmax()
        worst_month = monthly_patterns['y'].idxmin()
        
        print(f"\nMejor mes: {best_month} (Conversión: {monthly_patterns.loc[best_month, 'y']:.2%})")
        print(f"Peor mes: {worst_month} (Conversión: {monthly_patterns.loc[worst_month, 'y']:.2%})")
        
        return monthly_patterns
    
    return None

def generar_reporte_avanzado(df):
    """Genera reporte completo de análisis avanzado"""
    print("\nGenerando Reporte Avanzado...")
    
    # 1. Segmentación
    segment_df, clusters = segmentar_clientes(df)
    
    # 2. Análisis de cohortes
    cohortes = analisis_cohortes(df)
    
    # 3. ROI de campañas
    roi_campanas = analisis_roi_campanas(df)
    
    # 4. Estacionalidad
    estacionalidad = analisis_estacionalidad(df)
    
    # 5. Guardar resultados
    segment_df.to_csv('../data/processed/clientes_segmentados.csv', index=False)
    roi_campanas.to_csv('../data/processed/roi_campanas.csv')
    
    print("\nReporte Avanzado Completado!")
    print("Archivos generados:")
    print("   - clientes_segmentados.csv")
    print("   - roi_campanas.csv")
    print("   - cohortes_temporales.png")
    
    return {
        'segmentacion': segment_df,
        'cohortes': cohortes,
        'roi': roi_campanas,
        'estacionalidad': estacionalidad
    }

def main():
    """Función principal"""
    print("Iniciando Análisis Avanzado - Marketing Bancario")
    print("=" * 60)
    
    try:
        # Cargar datos procesados
        df = pd.read_csv('../data/processed/bank_customers_merged.csv')
        print(f"Datos cargados: {df.shape}")
        
        # Ejecutar análisis avanzado
        resultados = generar_reporte_avanzado(df)
        
        print("\nAnálisis avanzado completado exitosamente!")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 