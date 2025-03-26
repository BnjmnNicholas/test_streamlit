import streamlit as st
import pandas as pd
import pymysql
from datetime import timedelta
from datetime import datetime
from scipy.optimize import fsolve
from itertools import cycle
# tomamos las credenciales de .env
import os
from dotenv import load_dotenv
# ignore warnings
import warnings
warnings.filterwarnings("ignore")


host_creditos = st.secrets["host_creditos"]
port_creditos = int(st.secrets["port_creditos"])  # Convertir a entero
user_creditos = st.secrets["user_creditos"]
password_creditos = st.secrets["password_creditos"]
database_creditos = st.secrets["database_creditos"]


print(host_creditos, port_creditos, user_creditos, password_creditos)  


def get_connection():
    return pymysql.connect(
        host=host_creditos,
        port=port_creditos,
        user=user_creditos,
        password=password_creditos,
        database=database_creditos
    )

def fetch_data(koen):
    query = f"""
    SELECT Facturas, Koen, Nombre, Fecha_Vencimiento, Monto, Estado
    FROM tabla_creditos
    JOIN creditos_new.tabla_clientes tc ON tabla_creditos.Cliente_ID = tc.Cliente_ID
    WHERE Estado IN ('Default', 'Emitido')
    AND Koen LIKE '%{koen}%';
    """
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Interfaz en Streamlit
st.title("Búsqueda de Créditos por Koen")
koen_input = st.text_input("Ingrese Koen para buscar:")

if st.button("Buscar"):
    if koen_input:
        df_result = fetch_data(koen_input)
        if not df_result.empty:
            st.dataframe(df_result)
        else:
            st.warning("No se encontraron resultados para la búsqueda.")
    else:
        st.error("Ingrese un valor para Koen.")


