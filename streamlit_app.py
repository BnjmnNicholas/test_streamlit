import requests
import streamlit as st

def get_public_ip():
    try:
        ip = requests.get("https://api64.ipify.org?format=json").json()["ip"]
        return ip
    except Exception as e:
        return f"Error obteniendo IP: {e}"

st.write("IP pública del servidor de Streamlit:")
st.write(get_public_ip())


