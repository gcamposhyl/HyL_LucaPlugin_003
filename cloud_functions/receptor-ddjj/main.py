# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app


# initialize_app()
#
#
# duplico planilla y la inserto en carpeta
# @https_fn.on_request()
# def core_plugin_v1_duplicate_gsheet(req: https_fn.Request) -> https_fn.Response:
#     body = req.json
#     try:

#         folder_id = body["folder_id"] # id carpeta root
#         folder_name = body["plugin_name"] # nombre plugin        
#         user_id = body["user_id"] # id ususario
#         card_id = body["card_id"] # id tarjeta lanzadas

#         return https_fn.Response("objeto", content_type="application/json")
    
#     except Exception as ex:
#             print(str(ex)) 