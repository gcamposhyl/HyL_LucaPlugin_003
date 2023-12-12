import os
from io import StringIO
from io import BytesIO
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build



class Connection_drive:
    def __init__(self) -> None:
        pass

    def read_sheet_drive(self, name_sheet, range_data):
        try:

            cred = 'config/lucaplugs-sa.json'
            scopes=['https://www.googleapis.com/auth/spreadsheets']

            # Configuración de autenticación con la cuenta de servicio
            credents = service_account.Credentials.from_service_account_file(cred, scopes = scopes)

            # Crear un cliente de Google Sheets
            sheets_service = build('sheets', 'v4', credentials=credents)

            # Especificar la hoja de cálculo donde deseas escribir
            spreadsheet_id = os.environ.get('SHEET_PARAM_ID')
            # Rango de celdas que deseas leer (por ejemplo, 'Sheet1!A1:B10')
            range_ = f'{name_sheet}!{range_data}'

            # Llamada a la API de Google Sheets para obtener los valores
            result = sheets_service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_).execute()
            # Obtener los valores de las celdas
            values = result.get('values', [])
            df_values = pd.DataFrame(values[1:], columns=values[0])
            return df_values
        except Exception as error :
           print("Error in read_sientos_in_drive()", error) 
