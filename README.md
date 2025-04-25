# BFOA Mejorado - Algoritmo de Forrajeo de Bacterias para Alineamiento de Secuencias

Este repositorio contiene la implementación mejorada del algoritmo BFOA (Bacterial Foraging Optimization Algorithm), enfocado en el alineamiento de secuencias biológicas utilizando puntuaciones BLOSUM62 y técnicas de paralelismo.

---

## Características del algoritmo mejorado
- Mutación controlada durante el reemplazo de la peor bacteria.
- Evaluación con matriz BLOSUM62.
- Cálculo de interacción corregido para evitar overflow numérico.
- Soporte para ejecución paralela de evaluaciones (multiprocessing).

---

## Estructura del proyecto

```
BFOA-Mejorado/
├── bacteria.py                     # Clase principal con operadores del algoritmo
├── evaluadorBlosum.py             # Evaluador BLOSUM62
├── fastaReader.py                 # Lector de archivos multi-FASTA
├── analisis_parallel_BFOA_mejorado.py  # Script de ejecución y análisis de 30 corridas
├── multifasta.fasta               # Archivo de entrada con secuencias biológicas
├── resultados_BFOA_mejorado.csv   # Resultados guardados tras ejecución
├── README.md
```

---

## Requisitos

- Python 3.9 o superior
- numpy
- pandas
- matplotlib
- seaborn

Puedes instalarlos usando:
```bash
pip install numpy pandas matplotlib seaborn
```

---

## Ejecución del algoritmo

Desde terminal, ubícate en el directorio del proyecto y ejecuta:
```bash
python analisis_parallel_BFOA_mejorado.py
```
Esto realizará 30 corridas del algoritmo y generará el archivo `resultados_BFOA_mejorado.csv` con:
- Fitness final
- Tiempo de ejecución
- Score BLOSUM
- Interacción total

---

## Comparación con versión original
Incluye análisis estadístico y gráficas que comparan los resultados del algoritmo original con la versión mejorada. 
Para visualizar los resultados, se recomienda usar el notebook de comparación.

---

## Autor y crédito
Este proyecto fue desarrollado como parte de la asignatura "Administración de Proyectos de Software".

> Autor: Edwar Godina  
> Fecha: Abril 2025  
> Universidad: [Nombre de tu universidad aquí]

---

## ✅ Licencia
Este proyecto está disponible bajo la licencia MIT.
