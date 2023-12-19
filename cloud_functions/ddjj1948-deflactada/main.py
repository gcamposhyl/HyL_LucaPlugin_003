# componentes de negocio
from firebase_functions import https_fn

# librerias firebase
from components.controllers.main import Ddjj_1948
from firebase_functions.firestore_fn import (
  on_document_created,
  Event,
  Change,
  DocumentSnapshot,
)

# punto de entrada cloud functions!
@on_document_created(max_instances=10, document="ddjj/{userId}/1948/{cardId}/current_custom/config")
def plugin_v1_ddjj1948_deflactada(event: Event[Change[DocumentSnapshot]]) -> None:
    import json

    try:
        #datos de input
        inputs = event.data.to_dict()
        user_id = event.params["userId"]
        card_id = event.params["cardId"]
        output_sheet_id = inputs["drive_id"] # id de planilla 
        ipc_dic = inputs["ipc"]
        input_rut = inputs["rut"]
        input_year = inputs["year"]
        client_name = inputs["client_name"]
        ddjj_data = inputs["custom"]
        
        input_custom_corregido = ddjj_data.replace("'", '"') # formateo de fato para manipular lista

        try:
            # Intenta cargar el string JSON corregido
            ddjj_list = json.loads(input_custom_corregido)

        except json.JSONDecodeError as e:
            # Manejar la excepción en caso de un error de decodificación JSON
            return https_fn.Response(f"error input arreglo: {str(ex)}")
        
        # lógica ddjj deflactada
        ddjj_deflactada = Ddjj_1948(user_id, card_id, ipc_dic, input_year) # clase controladora
        ddjj_deflactada.get_ddjj1948(output_sheet_id, input_rut, client_name, ddjj_list) # ejecución de lógica

        return https_fn.Response("ok")
    
    except Exception as ex:
        return https_fn.Response(f"error: {str(ex)}")
    