from components.utils.gsheetUtil import Gsheet
from components.utils.driveUtil import Drive

import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()


class Ddjj_1948:

    def __init__(self, sc_id, sc_name) -> None:
        self._sc_id = sc_id
        self._sc_name = sc_name

    # id planilla con datos de scraping
    def get_sc_id(self):
        try:
            return self._sc_id
        except Exception as ex:
            print(str(ex)) 

    # nombre planilla con datos de scraping
    def get_sc_name(self):
        try:
            return self._sc_name
        except Exception as ex:
            print(str(ex)) 

    def get_ddjj1948(self):
        gsheet = Gsheet()
        # ESTAS VARIABLES VIENEN EN EL MENSAJE, SOLO ESTAN PARA TEST

        USER_ID = "123456"

        CARD_ID = "456789"

        TEMPLATE_FOLDER_ID = "1crLw_nmcOXYtVElAfxJgNuqQEs-G-1wv"

        OUTPUT_FOLDER_ID = "1F496ZgJi6I_Pn0NQvOmklIgYJ649B17L"

        PLUGIN_NAME = "ddjj_outputs"

        # id de carpeta donde se dejan los archivos nuevos
        current_folder = self.get_folder_id(OUTPUT_FOLDER_ID, PLUGIN_NAME, USER_ID, CARD_ID) # dicionario con id de carpeta

        # obtengo datos de scraping, aqui me llagara este mensaje, solo es para test
        scraping_data = gsheet.getSheetByNameSheet(self.get_sc_id(), self.get_sc_name())

        # obtengo template planilla
        year = "2023" # test año de proceso solicitado
        
        try:    
            name_template = f"1948_estandar_{year}"         
            # transformo en df
            df_scraping_data = pd.DataFrame(scraping_data)

            # valido datos relevantes

            # transformo datos según negocio
            update_df = self.transform_data(df_scraping_data)

            # id de template de referencia
            temp_files = self.get_template_id(TEMPLATE_FOLDER_ID, name_template) # nombre e id de template según año

            # creo copia de planilla template
            new_ddjj_file = self.copy_template(current_folder["name_id_card_folder"], temp_files[1], "prueba archivo") # diccionario con id de carpeta

            id_new_file = new_ddjj_file['id_gsheet']
            sheet_name = '1948 Retiros y Div.'
            start_cell = 'B14'

            # inserto datos en copia
            gsheet.insert_data_to_sheet(id_new_file, sheet_name, update_df, start_cell)

            # no retorno nada, solo cambio estado de documento

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
                print("Solicitud exitosa")
                # Puedes imprimir la respuesta si es necesario
                return response.json()
            else:
                print(f"Error en la solicitud. Código de estado: {response.status_code}")
                print(response.text)
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
                print("Solicitud exitosa")
                # Puedes imprimir la respuesta si es necesario
                # print(response.json())
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

            # unir ruts
            df_02 = transform.join_rut(df_01)            

            # transformar a numero
            df_03 = transform.transform_to_num(df_02) # aqui se podria hacer esto en la planilla template

            # transformar listas
            df_04 = transform.transform_list(df_03)

            # eliminar columnas de soporte
            df_finally = transform.delete_supp_cols(df_04)

            #return df_finally
            return df_finally 
            
        except Exception as ex:
            print(str(ex)) 
