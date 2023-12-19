# componentes de negocio
from components.utils.gsheetUtil import Gsheet
from components.utils.driveUtil import Drive

# librerias firebase
import firebase_admin
firebase_admin.initialize_app()

# librerias de utilidad
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()


class Ddjj_1948:

    def __init__(self, user_id, card_id, year) -> None:
        self._user_id = user_id
        self._card_id = card_id
        self._year = year


    def get_year(self):
        try:
            return self._year
        except Exception as ex:
            raise Exception(str(ex))

    def get_user_id(self):
        try:
            return self._user_id
        except Exception as ex:
            raise Exception(str(ex))

    def get_card_id(self):
        try:
            return self._card_id
        except Exception as ex:
            raise Exception(str(ex))

    def get_ddjj1948(self, current_sheet, rut, client_name, scraping_data):
        from datetime import datetime
        gsheet = Gsheet()
        
        try:    
            #PASO 1: MANIPULACION Y TRANSFORMACION DE INPUTS            
            df_scraping_data = pd.DataFrame(scraping_data) # transformo en df            
            update_df = self.transform_data(df_scraping_data) # transformo datos según negocio

            # PASO 2: INSERTAR DATOS DDJJ

            sheet_name = '1948 Retiros y Div.'
            start_cell = 'B14'            
            gsheet.insert_data_to_sheet(current_sheet, sheet_name, update_df, start_cell) # inserto datos ddjj en copia
            
            # PASO 3: INSERTAR DATOS DE CABECERA
            
            header_cell = 'B1'
            date_extract = datetime.now().strftime("%d/%m/%Y")
            header_matrix = [[f"Nombre Cliente: {client_name}"],
                             [f"RUT Cliente: {rut}"],
                             [f"Año Tributario: {self.get_year()}"],
                             [f"Fecha Extracción: {date_extract}"]]            
            header_df = pd.DataFrame(header_matrix)            
            gsheet.insert_data_to_sheet(current_sheet, sheet_name, header_df, header_cell)
            
            # PASO 4: INFORMAR PROCESO COMPLETADO

            self.confirm_sucess() # no retorno nada, solo cambio estado de documento


        except Exception as ex:
            raise Exception(str(ex))

    def confirm_sucess(self):
        from firebase_admin import firestore
        db = firestore.client()
        try:
            #* Obtención de datos desde firestore
            doc_estandar = db.collection("ddjj").document(str(self.get_user_id())).collection("1948").document(str(self.get_card_id())).collection("tasks").document("estandar")
            doc_estandar.set({"status": True}, merge=True)
        except Exception as ex:
            raise Exception(str(ex))

    def transform_data(self, df):

        from components.services.ddjjService import Transform
        transform = Transform()
        try:
            # formatear headers 
            df_01 = transform.to_format(df)
         
            # transformar a numero
            df_03 = transform.transform_to_num(df_01) # aqui se podria hacer esto en la planilla template

            # transformar listas
            df_finally = transform.transform_list(df_03)

            return df_finally 
            
        except Exception as ex:
            raise Exception(str(ex))
