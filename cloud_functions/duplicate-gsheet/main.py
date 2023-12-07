# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app
from components.controllers.main import File_manager

# initialize_app()
#
#
# duplico planilla y la inserto en carpeta
@https_fn.on_request(max_instances=10)
def core_plugin_v1_duplicate_gsheet(req: https_fn.Request) -> https_fn.Response:
    import json
    body = req.json
    try:

        folder_id = body["folder_id"] # id carpeta
        gsheet_id = body["gsheet_id"] # id planilla        
        name_gsheet = body["name_gsheet"] # nombre planilla

        id = File_manager().copy_file(folder_id, gsheet_id, name_gsheet)

        data = {
             "id_gsheet": id
        }

        # Convertir el diccionario a una cadena JSON
        json_data = json.dumps(data)

        return https_fn.Response(json_data, content_type="application/json")
    
    except Exception as ex:
            print(str(ex.with_traceback)) 