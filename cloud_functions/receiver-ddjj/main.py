
from firebase_functions import https_fn, pubsub_fn


@pubsub_fn.on_message_published(max_instances=10, topic="ddjj1948")
def plugin_v1_ddjj1948_receiver(event: pubsub_fn.CloudEvent[pubsub_fn.MessagePublishedData]) -> None:
    """Pub/Sub Cloud Function.
    """
    from components.utils.resources import Cloud_elements
    from components.utils.resources import Firebase_resources

    try:
        import requests
        import json
        import os
        import gc

        firebase_resources = Firebase_resources()
        ipc_url = os.environ.get('REQUEST_IPC')
    
        data = event.data.message.json
        custom = data["custom"]
        drive_id = data["drive_id"]
        
        card_id = data["card_id"]
        user_id = data["user_id"]

        # Obtener rut y año de cadena
        input_text = data["input_text"]
        string_files = input_text.replace("'", '"')
        input_text_list = json.loads(string_files)
        rut = str(input_text_list[0])
        year = str(input_text_list[1])
        params = {"year": year}

        # solicitar IPC
        ipc = {}
        response = requests.get(ipc_url, params=params)
        if response.status_code == 200:
            data_ipc = response.json()
            ipc = data_ipc["ipc"]
        else:
            data_ipc = response.json()
            ipc = data_ipc["error"]
            print(f"Error: {response.status_code}")

        #ipc dummy, luego sera sustituido por una petición a la interfaz core
        # ipc = {
        #     "enero": 0.9,
        #     "febrero": 1.1,
        #     "marzo": 1.09,
        #     "abril": 0.85,
        #     "mayo": 0.7,
        #     "junio": 1.25,
        #     "julio": 0.9,
        #     "agosto": 0.92,
        #     "septiembre": 0.85,
        #     "octubre": 0.7,
        #     "noviembre": 0.7,
        #     "diciembre": 1.1
        # }

        config = {
            "rut": rut,
            "year": year,
            "ipc": ipc,
            "custom": custom,
            "drive_id": drive_id
        }

        task = {
            "status": False
        }

        #limpia memoria hasta este punto
        gc.collect()

        firebase_resources.create_document(user_id, card_id, task, "tasks", "deflactada")
        firebase_resources.create_document(user_id, card_id, task, "tasks", "estandar")
        firebase_resources.create_document(user_id, card_id, config, "current_custom", "config")

    except Exception as e:
        print("Error en receiver:", str(e))
        return f"Error interno del servidor en moderator: {str(e)}", 500
