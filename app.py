import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from utils import grafica_1, descriptivo, grafica_2, filtro, tasa_aprobacion_temprana, tasa_perdida, importacion_datos, serie_tiempo, check_password

#autenticación
password = st.secrets['password']
key1 = st.secrets['key1']
key2 = st.secrets['key2']

if check_password() != True:
    st.stop()
    
#importación de datos
df = importacion_datos(key1, key2)

#encabezado
st.title('Facultad de Economía')
st.header('Comportamiento del desempeño académico de la Facultad de Economía para los años 2020-2021')

#definición y filtros
cols = ['periodo','depto','nom_materia','docente','apellidos_y_nombres','nivel_est']
nombres = ['Periodo',
            'Departamento',
            'Espacio',
            'Docente',
            'Estudiante',
            'Semestre']


for col, nombre in zip(cols, nombres):
    filtros = st.sidebar.multiselect(f'{nombre}', list(df[col].unique()) + ['Todos'], 'Todos')
    if 'Todos' not in filtros:
        df = filtro(df, col, filtros)


#gráficas

st.pyplot(grafica_1(df))
col1, col2 = st.columns(2)

col1.write(descriptivo(df))
col2.pyplot(grafica_2(df))

st.subheader(f'Aprobación temprana promedio: {tasa_aprobacion_temprana(df)}')


if df['periodo'].nunique() != 1:
    st.pyplot(serie_tiempo(df, 'aprob'))
    

st.subheader(f'Tasa de no aprobación promedio: {tasa_perdida(df)}')

if df['periodo'].nunique() != 1:
    st.pyplot(serie_tiempo(df, 'no_aprob'))


#notas al pie de pa´gina

st.write('*Al seleccionar la opción "Todos" en una variable junto con otras opciones, el aplicativo ignora las otras opciones y sigue presentando información con la categoría "Todos" para la variable.')
st.write('**Tasa de aprobación temprana: porcentaje de personas que aprueban una materia antes del tercer corte')
st.write('***Tasa de no aprobación: porcentaje de personas que no superan la nota mínima de aprobación')
st.write('****Existen valores de cero (0) que se deben a no ingreso de las notas a tiempo o dinámica propia del departamento encargado')
