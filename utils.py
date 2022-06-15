from os import remove
import boto3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from io import BytesIO

def tasa_perdida(df):
    a = df['no_aprob'].mean()
    return f'{round(a * 100, 2)}%'

def tasa_aprobacion_temprana(df):
    a = df['aprob'].mean()
    return f'{round(a * 100, 2)}%'

def importacion_datos(key1, key2):
    s3 = boto3.resource('s3', region_name='us-east-1',
                    aws_access_key_id=key1,
                    aws_secret_access_key=key2)
    bucket = s3.Bucket('test-bucket-transport')
    lista = list(bucket.objects.all())
    return pd.read_csv(BytesIO(lista[-3].get()['Body'].read()))

def descriptivo(df):
    a = df[['nota_1','nota_2','nota_3','definitiva']]
    a.columns = ['1er', '2do', '3er', 'def']
    return a.describe()

def remover_bordes(ax):
    for a in ax:
        a.spines['top'].set_visible(False)
        a.spines['right'].set_visible(False)
    return ax

def grafica_1(df):
    a = df[['nota_1','nota_2','nota_3','definitiva']]

    a = (a.stack()
            .reset_index()
            .set_index('level_0')
            .rename(columns={'level_1':'periodo',
                             0:'nota'}))

    fig, ax = plt.subplots(1, 2, figsize=(14, 8), sharey=True)
    sns.violinplot(data=a, x='periodo', y='nota', ax=ax[0], palette='mako')
    sns.boxplot(data=a, x='periodo', y='nota', ax=ax[1], palette='mako')
    ax = remover_bordes(ax)
    for a in ax:
        a.set_xticklabels(['1er','2do','3er','Def.'], size=12)
        a.set_xlabel('Corte', size=12)
        a.set_ylabel('Nota', size=12)
        a.axhline(3, color='#02607A', ls='--', alpha=0.3)
        a.set_title('Distribución', size=16)
        a.set_yticklabels(['', 0, 1, 2, 3, 4, 5], size=12)
    

    return fig

def filtro(df, columna, valores):
    a = df[df[columna].isin(valores)]
    return a


def grafica_2(df):
    a = df[['definitiva']]
    
    fig, ax = plt.subplots(1,1, figsize=(10,10))
    sns.histplot(data=a, x='definitiva', color='#00485C')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.set_xlabel('Definitiva', size=16)
    ax.set_ylabel('Count', size=16)
    ax.set_xticklabels(['', 0, 1, 2, 3, 4, 5], size=16)
    return fig

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

def serie_tiempo(df, stat):
    periodos_unicos = df['periodo'].unique()
    dic_tasas = {}
    for periodo in periodos_unicos:
        filtro = df[df['periodo'] == periodo]
        dic_tasas[str(periodo)] = filtro[stat].mean()
    
    fig, ax = plt.subplots(figsize=(14,8))

    ax.scatter(dic_tasas.keys(), dic_tasas.values(), marker='v')
    for periodo, valor in dic_tasas.items():
        ax.text(periodo, valor + 0.003, f'{round(valor*100,2)}%', verticalalignment='center',fontsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    return fig

