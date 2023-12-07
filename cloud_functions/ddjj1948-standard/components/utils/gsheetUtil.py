from google.oauth2 import service_account

class Gsheet:
    def __init__(self) -> None:
        #import google.auth
        from googleapiclient.discovery import build        
        try:
            cred = 'components/config/lucaplugs-sa.json'
            scopes=['https://www.googleapis.com/auth/spreadsheets']

            # Configuración de autenticación con la cuenta de servicio
            creds = service_account.Credentials.from_service_account_file(cred, scopes = scopes)
                        
            #creds, _ = google.auth.default()
                        
            drive = build('sheets', 'v4', credentials=creds)
            
        except Exception as e:
            raise Exception(str(e))   
             
        self._gsheet = drive  

    def get_gsheets(self):
        try:
            return self._gsheet

        except Exception as ex:
            print(str(ex))

    def getSheetByNameSheet(self, sc_id, sc_name):

        try:
            sheet = self.get_gsheets().spreadsheets()

            result = (
                sheet.values()
                .get(spreadsheetId=sc_id, range=f"{sc_name}")  # Ajusta el rango según tus necesidades
                .execute()
            )
            values = result.get("values", [])

            if not values:
                print("No data found.")
                return

            # print("Name, Major:")
            # for row in values:
            #     # Print columns A and E, which correspond to indices 0 and 4.
            #     print(f"{row[0]}, {row[4]}")

            return values
        except Exception as ex:
            print(str(ex))

    def insert_data_to_sheet(self, spreadsheet_id, sheet_name, df, start_cell):
        try:
            # Obtener el servicio de hojas de cálculo
            sheet = self.get_gsheets().spreadsheets()

            # Convertir el DataFrame a una lista de listas para enviar a la hoja de cálculo
            values = df.values.tolist()

            # Obtener el rango para actualizar, comenzando desde la celda especificada
            range_to_update = f"{sheet_name}!{start_cell}"

            # Crear el cuerpo de la solicitud para la actualización
            body = {"values": values}

            # Realizar la actualización en la hoja de cálculo
            sheet.values().update(
                spreadsheetId=spreadsheet_id,
                range=range_to_update,
                body=body,
                valueInputOption="RAW"
            ).execute()

            print("Datos insertados correctamente en la hoja de cálculo.")

        except Exception as ex:
            print(f"Error al insertar datos en la hoja de cálculo: {str(ex)}")