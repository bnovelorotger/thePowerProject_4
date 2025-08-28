# Instrucciones de Uso del Proyecto de Análisis de Marketing Bancario

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno (Chrome, Firefox, Edge, etc.)

## Instalación

1. Clona o descarga este repositorio
2. Abre una terminal en la carpeta del proyecto
3. Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

## Ejecutar el Análisis de Datos

Antes de usar el dashboard, debes ejecutar el análisis de datos:

```bash
# Navega a la carpeta src
cd src

# Ejecuta el análisis
python eda.py
```

Esto generará los archivos necesarios en las carpetas `data/processed/` y `figures/`.

## Iniciar el Dashboard

Para iniciar el dashboard interactivo:

```bash
# Asegúrate de estar en la carpeta src
cd src

# Iniciar el dashboard
streamlit run dashboard.py
```

El dashboard se abrirá automáticamente en tu navegador predeterminado en:
```
http://localhost:8501
```

## Solución de Problemas Comunes

### Error: "No module named 'pandas'"
```bash
pip install pandas matplotlib seaborn openpyxl numpy jupyter
```

### Error: "FileNotFoundError: '../data/raw/bank-additional.csv'"
- Verificar que los archivos de datos estén en `data/raw/`
- Ejecutar desde la carpeta raíz del proyecto

### Error: "Permission denied" al guardar figuras
- Verificar permisos de escritura en la carpeta `figures/`
- Crear manualmente las carpetas si no existen

## Estructura Esperada Después de la Ejecución

```
eda_bank_marketing/
├── data/
│   ├── raw/                    #Datos originales
│   └── processed/              #Datos limpios (generados)
├── figures/                     #Visualizaciones (generadas)
├── notebooks/                   #Notebook de análisis
├── src/                        #Script automatizado
└── README.md                   #Documentación
```

## Resultados Esperados

- **5 visualizaciones** guardadas en `figures/`
- **3 datasets procesados** en `data/processed/`
- **Análisis completo** ejecutado y documentado

## Funcionalidades Adicionales

### Dashboard Interactivo
```bash
pip install -r requirements.txt
streamlit run src/dashboard.py
```

### Análisis Avanzado
```bash
pip install -r requirements.txt
python src/analisis_avanzado.py
```

### Presentación Ejecutiva
- Ver archivo `PRESENTACION_EJECUTIVA.md` para stakeholders

## Soporte

Si encuentras algún problema, verifica:
1. Python 3.8+ instalado
2. Dependencias instaladas
3. Archivos de datos en `data/raw/`
4. Permisos de escritura en el directorio 