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