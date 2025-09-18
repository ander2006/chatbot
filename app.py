import streamlit as st
import requests
import json
import plotly.express as px
import pandas as pd
import ast


# Inyecta el CSS para ocultar el botón de GitHub
hide_github_icon = """
<style>
.css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
.styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
.viewerBadge_text__1JaDK {
    display: none;
}
</style>
"""

st.markdown(hide_github_icon, unsafe_allow_html=True)

# URL de tu API de FastAPI
API_URL = "https://69d8f34c3944.ngrok-free.app/human_query"

# Título de la aplicación
st.title("🤖 Chatbot Reportes Dinámicos")

# Inicializa el historial de chat si no existe
if "messages" not in st.session_state:
    st.session_state.messages = []

# Muestra los mensajes del historial en pantalla
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Captura la entrada del usuario
if prompt := st.chat_input("Escribe tu mensaje aquí"):
    # Añade el mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Muestra el mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepara la petición a la API
data = {"human_query": prompt}
headers = {'Content-Type': 'application/json'}

if prompt != None :
# Envía la petición a la API de FastAPI
    try:
        answer = requests.post(API_URL, data=json.dumps(data), headers=headers)
        answer.raise_for_status() # Lanza un error para códigos de estado no exitosos
        api_response          = answer.json()["answer_text"]
        api_response_graphic  = answer.json()["answer_graphic"]
        api_response_type     = answer.json()["answer_type"]
        if api_response_type == '':
            api_response_type = '2'
                
    except requests.exceptions.RequestException as e:
        api_response = f"Error al conectar con la API: {e}"

    # Muestra la respuesta del asistente
    with st.chat_message("assistant"):
         st.markdown(api_response)

    # Añade la respuesta del asistente al historial
    st.session_state.messages.append({"role": "assistant", "content": api_response})

#   validar si debe construirse un gráfico
    if api_response_graphic != "null" and api_response_graphic != []:

        data = ast.literal_eval(api_response_graphic)
        df = pd.DataFrame(data)
  
        key_list = list(data.keys())

# Crear un gráfico de barras interactivo con Plotly Express
        if api_response_type == '1':

            if len(key_list) > 0:

                fig = px.pie(df, values=key_list[1], names=key_list[0], title='Gráfico')
            else:
                fig = px.pie(df, values=key_list[0], title='Gráfico')

        elif api_response_type == '2':

            if len(key_list) > 0:

                fig = px.bar(df, x=key_list[0], y=key_list[1], title='Gráfico')
        else:
                fig = px.bar(df, x=key_list[0], title='Gráfico')
    
        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig)
    
      





