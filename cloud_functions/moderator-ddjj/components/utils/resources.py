import os
import requests
import firebase_admin
from firebase_admin import firestore, credentials
import json
from io import BytesIO
import requests
#cred_path = os.path.abspath('config/lucaplugs-sa.json')
# cred = credentials.Certificate(cred_path)
cred = credentials.ApplicationDefault()
app = firebase_admin.initialize_app(cred)
db = firestore.client()

# cred = credentials.ApplicationDefault()
# db = firestore.client()


class Cloud_elements:
    def __init__(self) -> None:
        pass

    def obtain_folder_id(self, plugin_name, user_id, card_id):
        url = os.environ.get('CF_CREATE_FOLDER')
        folder_id = os.environ.get('FOLDER_DRIVE_ID')
        headers = {"Content-Type": "application/json"}

        params = {
            "folder_id": folder_id,
            "plugin_name": plugin_name,
            "user_id": user_id,
            "card_id": card_id
        }

        # Realizar la solicitud POST
        response = requests.post(url, json=params, headers=headers)
        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            result_url = response.json().get("name_id_card_folder")
            return result_url
        else:
            print(f"Error en obtain_folder_id {response.status_code}: {response.text}")
            return response.text

class Firebase_resources:
    def __init__(self) -> None:
        pass

    def create_custom(self, plugin_name, user_id, ddjj, card_id, message):

        try:
            coll_ddjj = db.collection(plugin_name).document(user_id).collection(ddjj)
            coll_custom = coll_ddjj.document(card_id).collection("current_custom")
            doc_config = coll_custom.document("config")
            doc_message = coll_custom.document("message")
            doc_message.set(message)

        except Exception as e:
            print("Error en create_custom:", str(e))
            return f"Error interno del servidor en create_custom: {str(e)}", 500

    def obtain_data_json(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lanza una excepción para errores HTTP

            json_data = response.json()

            # Verificar si json_data es una lista de listas
            if isinstance(json_data, list) and all(isinstance(row, list) for row in json_data):
                return json_data
            else:
                print(f"El contenido de la URL no es un arreglo de arreglos: {url}")

        except requests.RequestException as e:
            print(f"Error al descargar la URL {url}: {e}")

        # Si hay un error o la URL no tiene el formato esperado, retorna None
        return None