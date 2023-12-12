import os
import requests
import firebase_admin
from firebase_admin import firestore, credentials
#cred_path = os.path.abspath('config/lucaplugs-sa.json')
cred = credentials.ApplicationDefault()
#cred = credentials.Certificate(cred_path)
app = firebase_admin.initialize_app(cred)
# cred = credentials.ApplicationDefault()
db = firestore.client()

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
        # cred_path = os.path.abspath('config/lucaplugs-sa.json')
        # cred = credentials.Certificate(cred_path)
        # self.app = firebase_admin.initialize_app(cred)
        # self.db = firestore.client()

    def create_document(self, user_id, card_id, data, collection, document):
        try:
            coll_ddjj = db.collection("ddjj").document(user_id).collection("1948")
            coll_custom = coll_ddjj.document(card_id).collection(collection)
            doc_config = coll_custom.document(document)
            doc_config.set(data)

        except Exception as e:
            print("Error en create_custom:", str(e))
            return f"Error interno del servidor en create_custom: {str(e)}", 500