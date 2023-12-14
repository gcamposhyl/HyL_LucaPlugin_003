from components.utils.gsheetUtil import Gsheet
from components.utils.driveUtil import Drive

import pandas as pd
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import firestore

firebase_admin.initialize_app()
db = firestore.client()

import os
load_dotenv()


class Ddjj_1948:

    def __init__(self, user_id, card_id, ipc_dic) -> None:
        self._user_id = user_id
        self._card_id = card_id
        self._ipc_dic = ipc_dic


    def get_user_id(self):
        try:
            return self._user_id
        except Exception as ex:
            print(str(ex)) 

    def get_card_id(self):
        try:
            return self._card_id
        except Exception as ex:
            print(str(ex)) 

    def get_ipc_dic(self):
        try:
            return self._ipc_dic
        except Exception as ex:
            print(str(ex)) 

    def get_ddjj1948(self, current_folder, rut, year, client_name, scraping_data):
        from datetime import datetime
        gsheet = Gsheet()
        template_folder_id = os.getenv("TEMPLATE_FOLDER_ID")
        
        try:    
            name_template = f"1948_deflactada_{year}"         
            # transformo en df
            df_scraping_data = pd.DataFrame(scraping_data)

            # valido datos relevantes

            # transformo datos según negocio
            update_df = self.transform_data(df_scraping_data)

            # id de template de referencia
            temp_files = self.get_template_id(template_folder_id, name_template) # nombre e id de template según año

            # creo copia de planilla template
            new_ddjj_file = self.copy_template(current_folder, temp_files[1], "prueba archivo deflactada") # diccionario con id de carpeta

            id_new_file = new_ddjj_file['id_gsheet']
            sheet_name = '1948 Deflactada'
            start_cell = 'B14'

            # inserto datos ddjj en copia
            gsheet.insert_data_to_sheet(id_new_file, sheet_name, update_df, start_cell)

            # inserto datos de cabecara
            header_cell = 'B1'
            client_rut = rut # de planilla clientes
            year_trib = year # año input
            date_extract = datetime.now().strftime("%d/%m/%Y")

            header_matrix = [[f"Nombre Cliente: {client_name}"],
                             [f"RUT Cliente: {client_rut}"],
                             [f"Año Tributario: {year_trib}"],
                             [f"Fecha Extracción: {date_extract}"]]
            
            header_df = pd.DataFrame(header_matrix)
            
            gsheet.insert_data_to_sheet(id_new_file, sheet_name, header_df, header_cell)

            # no retorno nada, solo cambio estado de documento
            self.confirm_sucess()


        except Exception as ex:
            print(str(ex)) 

    def confirm_sucess(self):
        from firebase_admin import firestore
        db = firestore.client()
        try:
            #* Obtención de datos desde firestore
            doc_deflactada = db.collection("ddjj").document(str(self.get_user_id())).collection("1948").document(str(self.get_card_id())).collection("tasks").document("deflactada")
            doc_deflactada.set({"status": True}, merge=True)
        except Exception as ex:
            print(str(ex))

    def get_template_id(self, folder_id, template_name):
        
        try:
            name_id_files = Drive().get_files_in_folder(folder_id)

            matches = list(filter(lambda x: template_name in x[0], name_id_files))
            return matches[0] if matches else None
             
        except Exception as ex:
            print(str(ex)) 

    def get_folder_id(self, folder_id, plugin_name, user_id, card_id):
        import requests
        project_id = os.getenv("PLUGIN_PROJECT_ID")
        region = os.getenv("PLUGIN_PROJECT_REGION")
        try:
            url = f"https://{region}-{project_id}.cloudfunctions.net/core_plugin_v1_output_directories"
            # Parámetros que deseas enviar en el cuerpo de la solicitud
            payload = {
                'folder_id': folder_id,
                'plugin_name': plugin_name,
                'user_id': user_id,
                'card_id': card_id
            }

            # Realizar la solicitud POST
            response = requests.post(url, json=payload)

            # Verificar el código de respuesta
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error en la solicitud. Código de estado: {response.status_code}")
        except Exception as ex:
            print(str(ex))

    def copy_template(self, folder_id, gsheet_id, name_gsheet):
        import requests
        project_id = os.getenv("PLUGIN_PROJECT_ID")
        region = os.getenv("PLUGIN_PROJECT_REGION")
        try:
            url = f"https://{region}-{project_id}.cloudfunctions.net/core_plugin_v1_duplicate_gsheet"

            # Parámetros que deseas enviar en el cuerpo de la solicitud
            payload = {
                'folder_id': folder_id,
                'gsheet_id': gsheet_id,
                'name_gsheet': name_gsheet,
            }

            # Realizar la solicitud POST
            response = requests.post(url, json=payload)

            # Verificar el código de respuesta
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error en la solicitud. Código de estado: {response.status_code}")
                print(response.text)

        except Exception as ex:
            print(str(ex))

    def transform_data(self, df):

        from components.services.ddjjService import Transform
        transform = Transform()
        try:
            # formatear headers 
            df_01 = transform.to_format(df)

            # transformar a numero
            df_03 = transform.transform_to_num(df_01) # aqui se podria hacer esto en la planilla template

            # transformar listas
            df_04 = transform.transform_list(df_03)

            df_finally = transform.set_ipc(df_04, self.get_ipc_dic)

            return df_finally 
            
        except Exception as ex:
            print(str(ex)) 
