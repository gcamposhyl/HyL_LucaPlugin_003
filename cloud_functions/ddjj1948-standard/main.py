# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app
from components.controllers.main import Ddjj_1948


# initialize_app()
#
#
@https_fn.on_request()
def core_plugin_v1_ddjj1948(req: https_fn.Request) -> https_fn.Response:
    SPREADSHEET_ID = "1f_qE1FP5wmFFASAAWSUuDGY8_rP468qLiDUK3QR0FbI"
    SHEET_NAME= "Stage_AgeRet_DJ1948"
    try:
        Ddjj_1948(SPREADSHEET_ID, SHEET_NAME).get_ddjj1948()

        return https_fn.Response("Hello world!")
    
    except Exception as ex:
            print(str(ex)) 



# notas
# plugin guardara planilla de headers
# core guardara datos de ddjj, solo me devolvera datos de un rut especifico

# pasos
# obtengo datos de scraping
# valido datos respectivos
# transformo datos respectivos
# obtengo matriz ordenada
# consulto template segun año
# creo nuevo archivo con template como base
# inserto datos
# obtengo url de carpeta
# inserto en repo interno datos terminados

# modelos headers