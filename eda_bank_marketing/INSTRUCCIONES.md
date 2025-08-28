# Instrucciones Rápidas de Ejecución

## Ejecución Automatizada (Recomendada)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar análisis completo
cd src
python eda.py
```

## Ejecución Interactiva con Notebook

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Abrir notebook en VS Code
# Navegar a notebooks/eda.ipynb
# Ejecutar celdas secuencialmente
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
│   ├── raw/                    # ✅ Datos originales
│   └── processed/              # ✅ Datos limpios (generados)
├── figures/                     # ✅ Visualizaciones (generadas)
├── notebooks/                   # ✅ Notebook de análisis
├── src/                        # ✅ Script automatizado
└── README.md                   # ✅ Documentación
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
1. ✅ Python 3.8+ instalado
2. ✅ Dependencias instaladas
3. ✅ Archivos de datos en `data/raw/`
4. ✅ Permisos de escritura en el directorio 