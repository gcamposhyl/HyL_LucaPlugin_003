from google.oauth2 import service_account

class Drive:

    def __init__(self):
        from googleapiclient.discovery import build        
        try:
            creds = 'components/config/lucaplugs-sa.json'
            scopes=["https://www.googleapis.com/auth/drive.metadata.readonly",
                    "https://www.googleapis.com/auth/drive.file",
                    "https://www.googleapis.com/auth/drive"]

            # Configuración de autenticación con la cuenta de servicio
            creds = service_account.Credentials.from_service_account_file(creds, scopes = scopes)

            drive = build('drive', 'v3', credentials=creds)
            
        except Exception as e:
            raise Exception(str(e))   
             
        self._drive = drive  

    def get_drive(self):
        try:
            return self._drive

        except Exception as ex:
            print(str(ex))

    def create_folder(self, name, id):
        """
        Crea nueva carpeta y retorna id de carpeta creada
        input: name: nombre nueva carpeta
        input: id: id carpetta padre
        output: id carpeta creada
        """
        try:
            # Definir los metadatos de la nueva carpeta
            folder_metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [id]
            }

            # Crear la carpeta en Google Drive
            folder = self.get_drive().files().create(body=folder_metadata).execute()

            folder_id = folder["id"]

            return folder_id
        except Exception as ex:
            print(str(ex))
        
    def get_subfolders(self, id_folder: str):
        """
        Función obtiene nombre e id de carpetas dentro de carpeta padre
        """
        try:
            # Consultar las carpetas dentro de la carpeta padre
            results = self.get_drive().files().list(
                q=f"'{id_folder}' in parents and mimeType='application/vnd.google-apps.folder'",
                fields="files(name, id)"
            ).execute()
            
            subfolders = []
    
            items = results.get('files', [])
            for item in items:
                subfolder_name = item['name']
                subfolder_id = item['id']
                print(f"nombre: {subfolder_name}")
                print(f"id: {subfolder_id}")
                subfolders.append([subfolder_name, subfolder_id])

            return subfolders  
        
        except Exception as e:
            raise Exception(str(e))
        
    def get_files_in_folder(self, id_folder: str):
        """
        Función obtiene nombre e id de archivos dentro de carpeta padre
        """
        try:
            # Consultar los archivos dentro de la carpeta padre
            results = self.get_drive().files().list(
                q=f"'{id_folder}' in parents and mimeType!='application/vnd.google-apps.folder'",
                fields="files(name, id)"
            ).execute()

            files_list = []

            items = results.get('files', [])
            for item in items:
                file_name = item['name']
                file_id = item['id']
                #print(f"Nombre del archivo: {file_name}")
                #print(f"ID del archivo: {file_id}")
                files_list.append([file_name, file_id])

            return files_list

        except Exception as e:
            raise Exception(str(e))