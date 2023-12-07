# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from components.controllers.main import Folder_master

# initialize_app()

# recibe nombre de plugin, id de usuario e id de card, esto sera del core plugin
@https_fn.on_request(max_instances=10)
def core_plugin_v1_output_directories(req: https_fn.Request) -> https_fn.Response:
    body = req.json
    try:
        folder_id = body["folder_id"] # id carpeta root
        folder_name = body["plugin_name"] # nombre plugin        
        user_id = body["user_id"] # id ususario
        card_id = body["card_id"] # id tarjeta lanzadas

        new_card_id_folder = Folder_master().create_folder(folder_id, folder_name, user_id, card_id)

        return https_fn.Response(new_card_id_folder, content_type="application/json")
    
    except Exception as ex:
            print(str(ex)) 