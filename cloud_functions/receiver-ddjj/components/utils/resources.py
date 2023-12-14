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

    def obtain_matrice(self, dictionary):
        try:
            matrice = []
            order = ['COL01', 'COL02', 'COL03', 'COL04', 'COL05', 'COL06', 'COL07', 'COL08', 'COL09', 'COL10', 'COL11', 'COL12', 'COL13', 'COL14', 'COL15', 'COL16', 'COL17', 'COL18', 'COL19', 'COL20', 'COL21', 'COL22', 'COL23', 'COL24', 'COL25', 'COL26', 'COL27', 'COL28', 'COL29', 'COL30', 'COL31', 'COL32', 'COL33', 'COL34', 'COL35', 'COL36', 'COL37', 'COL38', 'COL39', 'COL40']
            matrice.append(order)
            for data in dictionary:
                ordered_row = [str(data[clave]) for clave in order]
                matrice.append(ordered_row)

            return matrice
        except Exception as error :
           print("Error in read_sientos_in_drive()", error)


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