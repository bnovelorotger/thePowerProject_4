#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script principal para Análisis Exploratorio de Datos - Marketing Bancario
Autor: Bernardo Novelo Rotger
Fecha: 28/08/2025
Descripción: Script automatizado para realizar EDA completo de datos de marketing bancario
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import os
import sys

# Configuración de visualización
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# Suprimir warnings
warnings.filterwarnings('ignore')

def configurar_directorios():
    """Configura los directorios necesarios para el proyecto"""
    dirs = ['../data/processed', '../figures']
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    print("Directorios configurados")

def cargar_datos():
    """Carga todos los datasets necesarios"""
    print("Cargando datos...")
    
    # Cargar dataset principal
    bank_df = pd.read_csv('../data/raw/bank-additional.csv')
    print(f"   - bank-additional.csv: {bank_df.shape}")
    
    # Cargar archivo Excel
    excel_file = '../data/raw/customer-details.xlsx'
    customer_sheets = pd.read_excel(excel_file, sheet_name=None)
    
    # Unificar hojas del Excel
    customers_list = []
    for sheet_name, df in customer_sheets.items():
        df['source_sheet'] = sheet_name
        customers_list.append(df)
    
    customers_df = pd.concat(customers_list, ignore_index=True)
    print(f"   - customer-details.xlsx: {customers_df.shape}")
    
    return bank_df, customers_df

def limpiar_bank_data(df):
    """Limpia y transforma el dataset de marketing bancario"""
    print("Limpiando datos de marketing bancario...")
    
    df_clean = df.copy()
    
    # Estandarizar nombres de columnas
    df_clean.columns = df_clean.columns.str.lower().str.replace('.', '_')
    
    # Convertir columnas binarias
    binary_columns = ['default', 'housing', 'loan', 'y']
    for col in binary_columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].map({'yes': 1, 'no': 0, 'y': 1, 'n': 0})
    
    # Convertir columnas macroeconómicas a numéricas
    numeric_columns = ['emp_var_rate', 'cons_price_idx', 'cons_conf_idx', 'euribor3m', 'nr_employed']
    for col in numeric_columns:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    # Parseo de fechas
    date_columns = ['date', 'contact_month', 'contact_year', 'dt_customer']
    for col in date_columns:
        if col in df_clean.columns:
            try:
                df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
            except:
                pass
    
    # Convertir duración a numérico
    if 'duration' in df_clean.columns:
        df_clean['duration'] = pd.to_numeric(df_clean['duration'], errors='coerce')
    
    print(f"Datos limpiados: {df_clean.shape}")
    return df_clean

def limpiar_customers_data(df):
    """Limpia y transforma el dataset de clientes"""
    print("Limpiando datos de clientes...")
    
    df_clean = df.copy()
    
    # Estandarizar nombres de columnas
    df_clean.columns = df_clean.columns.str.lower().str.replace('.', '_')
    
    # Convertir columnas numéricas
    numeric_columns = ['income', 'kidhome', 'teenhome', 'numwebvisitsmonth']
    for col in numeric_columns:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    # Parseo de fechas
    if 'dt_customer' in df_clean.columns:
        df_clean['dt_customer'] = pd.to_datetime(df_clean['dt_customer'], errors='coerce')
    
    print(f"Datos limpiados: {df_clean.shape}")
    return df_clean

def unir_datasets(bank_df, customers_df):
    """Une ambos datasets por ID"""
    print("Uniendo datasets...")
    
    # Renombrar columna ID para unificación
    if 'id_' in bank_df.columns and 'id' in customers_df.columns:
        merged_df = pd.merge(bank_df, customers_df, left_on='id_', right_on='id', how='inner')
        print(f"Datasets unidos: {merged_df.shape}")
        return merged_df
    else:
        print("No se encontraron columnas ID para unir")
        return None

def generar_estadisticas_descriptivas(df):
    """Genera estadísticas descriptivas básicas"""
    print("Generando estadísticas descriptivas...")
    
    # Estadísticas básicas para columnas numéricas
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    stats_basicas = df[numeric_cols].describe()
    
    # Tasa de conversión global
    if 'y' in df.columns:
        conversion_rate = df['y'].mean()
        print(f"Tasa de conversión global: {conversion_rate:.2%}")
    
    # Tasa de conversión por canal de contacto
    if 'contact' in df.columns and 'y' in df.columns:
        conversion_by_contact = df.groupby('contact')['y'].agg(['mean', 'count']).round(4)
        print("Tasa de conversión por canal de contacto:")
        print(conversion_by_contact)
    
    return stats_basicas

def generar_visualizaciones(df):
    """Genera todas las visualizaciones requeridas"""
    print("Generando visualizaciones...")
    
    # Configurar estilo
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # 1. Distribución de edad
    if 'age' in df.columns:
        plt.figure(figsize=(10, 6))
        plt.hist(df['age'].dropna(), bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        plt.title('Distribución de Edad de Clientes', fontsize=16, fontweight='bold')
        plt.xlabel('Edad', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.savefig('../figures/age_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("age_distribution.png generado")
    
    # 2. Distribución de contactos de campaña
    if 'campaign' in df.columns:
        plt.figure(figsize=(10, 6))
        plt.hist(df['campaign'].dropna(), bins=20, alpha=0.7, color='lightgreen', edgecolor='black')
        plt.title('Distribución de Número de Contactos por Campaña', fontsize=16, fontweight='bold')
        plt.xlabel('Número de Contactos', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.savefig('../figures/campaign_contacts_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("campaign_contacts_distribution.png generado")
    
    # 3. Tasa de conversión por canal de contacto
    if 'contact' in df.columns and 'y' in df.columns:
        conversion_data = df.groupby('contact')['y'].mean().sort_values(ascending=False)
        plt.figure(figsize=(10, 6))
        conversion_data.plot(kind='bar', color='coral', alpha=0.7)
        plt.title('Tasa de Conversión por Canal de Contacto', fontsize=16, fontweight='bold')
        plt.xlabel('Canal de Contacto', fontsize=12)
        plt.ylabel('Tasa de Conversión', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('../figures/conversion_by_contact.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("conversion_by_contact.png generado")
    
    # 4. Heatmap de correlaciones
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        correlation_matrix = df[numeric_cols].corr()
        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                   square=True, linewidths=0.5, cbar_kws={"shrink": .8})
        plt.title('Matriz de Correlación de Variables Numéricas', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('../figures/correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("correlation_heatmap.png generado")
    
    # 5. Tasa de conversión vs número de contactos
    if 'campaign' in df.columns and 'y' in df.columns:
        conversion_by_campaign = df.groupby('campaign')['y'].agg(['mean', 'count']).reset_index()
        conversion_by_campaign = conversion_by_campaign[conversion_by_campaign['count'] >= 5]  # Filtrar por frecuencia
        
        plt.figure(figsize=(10, 6))
        plt.scatter(conversion_by_campaign['campaign'], conversion_by_campaign['mean'], 
                   s=conversion_by_campaign['count']*2, alpha=0.7, color='purple')
        plt.title('Tasa de Conversión vs Número de Contactos', fontsize=16, fontweight='bold')
        plt.xlabel('Número de Contactos', fontsize=12)
        plt.ylabel('Tasa de Conversión', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('../figures/conversion_vs_contacts.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("conversion_vs_contacts.png generado")

def guardar_datos_procesados(bank_clean, customers_clean, merged_df):
    """Guarda los datasets procesados"""
    print("Guardando datos procesados...")
    
    bank_clean.to_csv('../data/processed/bank_clean.csv', index=False)
    customers_clean.to_csv('../data/processed/customers_clean.csv', index=False)
    
    if merged_df is not None:
        merged_df.to_csv('../data/processed/bank_customers_merged.csv', index=False)
        print("Todos los datasets guardados")
    else:
        print("Solo datasets individuales guardados")

def main():
    """Función principal que ejecuta todo el flujo de EDA"""
    print("Iniciando Análisis Exploratorio de Datos - Marketing Bancario")
    print("=" * 70)
    
    try:
        # 1. Configurar directorios
        configurar_directorios()
        
        # 2. Cargar datos
        bank_df, customers_df = cargar_datos()
        
        # 3. Limpiar y transformar datos
        bank_clean = limpiar_bank_data(bank_df)
        customers_clean = limpiar_customers_data(customers_df)
        
        # 4. Unir datasets
        merged_df = unir_datasets(bank_clean, customers_clean)
        
        # 5. Generar estadísticas descriptivas
        if merged_df is not None:
            stats = generar_estadisticas_descriptivas(merged_df)
        else:
            stats = generar_estadisticas_descriptivas(bank_clean)
        
        # 6. Generar visualizaciones
        if merged_df is not None:
            generar_visualizaciones(merged_df)
        else:
            generar_visualizaciones(bank_clean)
        
        # 7. Guardar datos procesados
        guardar_datos_procesados(bank_clean, customers_clean, merged_df)
        
        print("\nAnálisis Exploratorio de Datos completado exitosamente!")
        print("Los resultados se han guardado en las carpetas 'figures/' y 'data/processed/'")
        
    except Exception as e:
        print(f"Error durante la ejecución: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    main() 