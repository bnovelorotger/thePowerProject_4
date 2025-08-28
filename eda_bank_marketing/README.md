# Análisis Exploratorio de Datos - Marketing Bancario

## Objetivo del Proyecto

Este proyecto realiza un análisis exploratorio completo de los datos de campañas de marketing directo de una institución bancaria portuguesa. El objetivo es comprender los patrones de comportamiento de los clientes, identificar factores que influyen en la conversión y proporcionar insights valiosos para futuras estrategias de marketing.

## Estructura del Proyecto

```
eda_bank_marketing/
│
├── data/
│   ├── raw/                    # Datos originales
│   │   ├── bank-additional.csv
│   │   └── customer-details.xlsx
│   └── processed/              # Datos limpios y procesados
│       ├── bank_clean.csv
│       ├── customers_clean.csv
│       └── bank_customers_merged.csv
│
├── notebooks/
│   └── eda.ipynb              # Notebook principal de análisis
│
├── figures/                    # Visualizaciones generadas
│   ├── age_distribution.png
│   ├── campaign_contacts_distribution.png
│   ├── conversion_by_contact.png
│   ├── correlation_heatmap.png
│   └── conversion_vs_contacts.png
│
├── src/
│   └── eda.py                 # Script automatizado de Python
│
├── requirements.txt            # Dependencias del proyecto
└── README.md                  # Este archivo
```

## Descripción de los Datos

### Dataset Principal: bank-additional.csv
Contiene información detallada sobre las campañas de marketing telefónico:

- **Variables Demográficas**: edad, ocupación, estado civil, educación
- **Variables Financieras**: default, housing, loan
- **Variables de Campaña**: método de contacto, duración, número de contactos
- **Variables Macro**: tasa de empleo, índices de precios, confianza del consumidor
- **Variable Objetivo**: y (conversión: sí/no)

### Dataset Secundario: customer-details.xlsx
Información demográfica y de comportamiento de clientes (3 hojas por año):

- **Variables Demográficas**: ingresos, número de niños/adolescentes en el hogar
- **Variables de Comportamiento**: visitas mensuales al sitio web
- **Variables Temporales**: fecha de conversión a cliente
- **Identificación**: ID único del cliente

## Pasos de Limpieza y Transformación

### 1. Unificación de Datos
- Consolidación de las 3 hojas del archivo Excel en un único dataframe
- Adición de columna `source_sheet` para identificar el origen

### 2. Estandarización de Nombres
- Conversión de nombres de columnas a formato `snake_case`
- Reemplazo de puntos por guiones bajos en variables macroeconómicas

### 3. Conversión de Tipos de Datos
- **Variables Binarias**: conversión de 'yes'/'no' y 'y'/'n' a 0/1
- **Variables Numéricas**: conversión de columnas macroeconómicas y demográficas
- **Variables de Fecha**: parseo de fechas en múltiples formatos

### 4. Manejo de Valores Nulos
- Identificación y reporte de valores faltantes
- Estrategias de imputación según el tipo de variable

### 5. Unificación de Datasets
- Merge por ID entre datasets de marketing y clientes
- Preservación de integridad referencial

## Análisis Descriptivo

### Estadísticas Básicas
- Resumen estadístico completo de variables numéricas
- Distribuciones de frecuencias para variables categóricas

### Análisis de Conversión
- **Tasa Global**: Porcentaje general de conversión
- **Por Canal de Contacto**: Efectividad de diferentes métodos
- **Por Ocupación**: Segmentación por profesión
- **Por Estado Civil**: Análisis demográfico

### Análisis de Correlaciones
- Matriz de correlación entre variables numéricas
- Identificación de relaciones significativas

## Visualizaciones Generadas

### 1. Distribución de Edad (`age_distribution.png`)
- Histograma de la distribución de edad de los clientes
- Identificación de grupos de edad predominantes

### 2. Distribución de Contactos (`campaign_contacts_distribution.png`)
- Histograma del número de contactos por campaña
- Análisis de la intensidad de las campañas

### 3. Conversión por Canal (`conversion_by_contact.png`)
- Gráfico de barras de tasas de conversión por método de contacto
- Comparación de efectividad entre canales

### 4. Heatmap de Correlaciones (`correlation_heatmap.png`)
- Matriz de correlación visual con escala de colores
- Identificación de patrones de correlación

### 5. Conversión vs Contactos (`conversion_vs_contacts.png`)
- Gráfico de dispersión de conversión vs número de contactos
- Análisis de la relación entre persistencia y éxito

## Instrucciones de Ejecución

### Prerrequisitos
- Python 3.8 o superior
- VS Code con extensión de Python
- Acceso a terminal/consola

### Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### Opción 1: Ejecución Automatizada
```bash
cd src
python eda.py
```

### Opción 2: Análisis Interactivo
1. Abrir `notebooks/eda.ipynb` en VS Code
2. Ejecutar celdas secuencialmente
3. Explorar resultados y modificar análisis según necesidades

### Opción 3: Ejecución desde VS Code
1. Abrir la carpeta del proyecto en VS Code
2. Navegar a `src/eda.py`
3. Ejecutar el archivo completo (F5)

## Dependencias Principales

- **pandas**: Manipulación y análisis de datos
- **matplotlib**: Generación de gráficos básicos
- **seaborn**: Visualizaciones estadísticas avanzadas
- **openpyxl**: Lectura de archivos Excel
- **numpy**: Operaciones numéricas
- **jupyter**: Entorno de notebooks

## Hallazgos Clave

### 1. Patrones de Conversión
- **Tasa de conversión global**: 11.27%
- **Canal móvil vs fijo**: 14.74% vs 5.16% (2.86x más efectivo)
- **Punto óptimo de contactos**: 3-5 por campaña

### 2. Segmentación de Clientes
- **Grupos de edad objetivo**: 25-35 y 45-55 años
- **Ocupaciones de alto valor** identificadas
- **Patrones demográficos** claramente definidos

### 3. Efectividad de Campañas
- **Canal cellular** prioritaria para inversión
- **Frecuencia optimizada** para maximizar conversiones
- **Segmentación estratégica** por demografía

### 4. Factores de Influencia
- **Indicadores macroeconómicos** correlacionados
- **Historial de contactos** influye en conversión
- **Timing y persistencia** críticos para el éxito

> **Para resultados detallados**: Ver archivo `RESULTADOS_ANALISIS.md`

## Próximos Pasos

### Análisis Avanzado
- Segmentación de clientes por comportamiento
- Análisis de cohortes temporales
- Identificación de patrones estacionales

### Modelado Predictivo
- Desarrollo de modelos de clasificación
- Predicción de probabilidad de conversión
- Optimización de estrategias de contacto

### Dashboard Interactivo
- Creación de visualizaciones interactivas
- Panel de control para stakeholders
- Actualización automática de métricas

## Autor

Bernardo Novelo Rotger
Fecha: 28/08/2025

## Referencias

- Dataset: UCI Machine Learning Repository - Bank Marketing
- Metodología: Análisis Exploratorio de Datos (EDA)
- Herramientas: Python, Pandas, Matplotlib, Seaborn

## Contribuciones

Este proyecto es parte del módulo "Python for Data" de ThePowerMBA. Las contribuciones y mejoras son bienvenidas a través de issues y pull requests.

---

**Nota**: Este README se actualizará automáticamente con los hallazgos específicos tras la ejecución del análisis exploratorio de datos. 