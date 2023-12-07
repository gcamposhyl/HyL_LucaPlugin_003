from components.utils.driveUtil import Drive

class Folder_master:
    def __init__(self) -> None:
        pass

    def create_folder(self, folder_id, folder_name, user_id, card_id):
        import json
        try:

            drive = Drive()

            # validar si existe
            root_folders = drive.get_subfolders(folder_id)
            if(len(root_folders) == 0 ):
                new_folder_id = drive.create_folder(folder_name, folder_id) # creo carpeta con nombre de plugin
            else:
                new_folder_id = root_folders[0][1]
            
            # validar si existe
            user_folders = drive.get_subfolders(new_folder_id)
            # crear carpeta egresos/userId
            if(len(user_folders) == 0 ):
                user_folder = drive.create_folder(user_id, new_folder_id)
            else:
                user_folder = user_folders[0][1]
            
            card_folder = drive.create_folder(card_id, user_folder)

            new_folder = {
                "name_id_card_folder": card_folder
            }

            # Convertir el diccionario a una cadena JSON
            return json.dumps(new_folder)
        
        except Exception as ex:
            print(str(ex))