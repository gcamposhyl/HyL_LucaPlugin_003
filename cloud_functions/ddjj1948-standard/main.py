from firebase_functions import https_fn
from firebase_admin import initialize_app
from components.controllers.main import Ddjj_1948

# from firebase_functions.firestore_fn import (
#   on_document_updated,
#   Event,
#   Change,
#   DocumentSnapshot,
# )
# import firebase_admin
# from firebase_admin import firestore

# app = firebase_admin.initialize_app()

# @on_document_updated(max_instances=10, document="{pluginName}/{plugindId}/{cardId}/{messageId}")
# def core_plugin_v1_ddjj1948(event: Event[Change[DocumentSnapshot]]) -> None:
@https_fn.on_request()
def core_plugin_v1_ddjj1948(req: https_fn.Request) -> https_fn.Response:
    # variables planilla de scraping, se deben borrar
    SPREADSHEET_ID = "1f_qE1FP5wmFFASAAWSUuDGY8_rP468qLiDUK3QR0FbI"
    SHEET_NAME= "Stage_AgeRet_DJ1948"
    try:
        Ddjj_1948(SPREADSHEET_ID, SHEET_NAME).get_ddjj1948()

        return https_fn.Response("ok")
    
    except Exception as ex:
        print(str(ex)) 
        return https_fn.Response(f"error: {str(ex)}")
