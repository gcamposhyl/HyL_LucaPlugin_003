import os
import requests
import datetime
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

    def validate_year(self, year):
        if not year.isdigit():
            raise ValueError("El año debe contener solo números.")
        
        # Obtener el año actual
        ano_actual = datetime.datetime.now().year

        # Convertir la entrada a entero y asegurarse de que tenga 4 dígitos
        year = int(year)
        if len(str(year)) != 4:
            raise ValueError("El año debe tener 4 dígitos.")
        
        # Verificar que el año no sea superior al actual
        if year > ano_actual:
            raise ValueError("No se puede consultar un año superior al actual.")
        
        # Verificar que el año esté dentro de un rango de 10 años
        if ano_actual - year > 10:
            raise ValueError("El año debe estar dentro de un rango de 10 años respecto al actual.")

        # Si todas las condiciones son correctas, retornar el año
        return year


    def rut_without_points(self, rut):
        rut_str = str(rut).replace(" ", "")
        rut_str = rut_str.replace(".", "").replace("-", "")

        if len(rut_str) < 8 or len(rut_str) > 9:
            raise ValueError("El RUT debe tener entre 8 y 9 números.")

        if not rut_str[:-1].isdigit() or (rut_str[-1].lower() != 'k' and not rut_str[-1].isdigit()):
            raise ValueError("Formato de RUT incorrecto, sólo puede contener como letra la 'K'.")

        rut_str = rut_str.lstrip("0")

        if len(rut_str) < 8:
            raise ValueError("El RUT debe tener al menos 8 números significativos.")

        rut_formateado = rut_str[:-1] + "-" + rut_str[-1].lower()
        # rut_str = str(rut).replace(" ", "")
        # rut_str = rut_str.replace(".", "").replace("-", "")

        # if not rut_str.isdigit():
        #     raise ValueError("Formato de RUT incorrecto, no debe contener letras.")
        
        # if len(rut_str) < 8 or len(rut_str) > 9:
        #     raise ValueError("Formato de RUT incorrecto, debe tener entre 8 y 9 números.")

        # rut_str = rut_str.lstrip("0")

        # if len(rut_str) < 8:
        #     raise ValueError("El RUT debe tener al menos 8 números significativos.")

        # rut_formateado = rut_str[:-1] + "-" + rut_str[-1]
        return rut_formateado

    def formatted_rut(self, input_string):
        guion_y_digito_final = input_string[-2:].upper()
        parte_numerica = input_string[:-2]

        if len(parte_numerica) == 8:
            parte_numerica_con_puntos = f"{parte_numerica[:2]}.{parte_numerica[2:5]}.{parte_numerica[5:]}"
        elif len(parte_numerica) == 7:
            parte_numerica_con_puntos = f"{parte_numerica[0]}.{parte_numerica[1:4]}.{parte_numerica[4:]}"
        else:
            raise ValueError("La longitud de la parte numérica no es válida.")

        resultado_final = f"{parte_numerica_con_puntos}{guion_y_digito_final}"
        return resultado_final
    
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