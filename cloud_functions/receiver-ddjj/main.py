
from firebase_functions import https_fn, pubsub_fn


@pubsub_fn.on_message_published(max_instances=10, topic="ddjj1948")
def plugin_v1_ddjj1948_receiver(event: pubsub_fn.CloudEvent[pubsub_fn.MessagePublishedData]) -> None:
    """Pub/Sub Cloud Function.
    """
    from components.utils.resources import Firebase_resources

    try:
        import requests
        import json
        import os
        import gc

        project_id = os.getenv("PROJECT_ID_FIREBASE")
        region = os.getenv("PLUGIN_PROJECT_REGION")
        request_client_name = f"https://{region}-{project_id}.cloudfunctions.net/plugin_v1_data_masters"
        request_ipc = f'https://{region}-luca-app-dev.cloudfunctions.net/core-v1-get_data_interface/getAllByYear'
        firebase_resources = Firebase_resources()
    
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
        params_ipc = {"year": year}
        params_client = {"rut": rut}

        # solicitar IPC
        ipc = {}
        response_ipc = requests.get(request_ipc, params=params_ipc)
        if response_ipc.status_code == 200:
            data_ipc = response_ipc.json()
            ipc = data_ipc["ipc"]
        else:
            data_ipc = response_ipc.json()
            ipc = data_ipc["error"]
            print(f"Error: {response_ipc.status_code}")


        # solicitar nombre de cliente
        client_name = ""
        response_client = requests.get(request_client_name, params=params_client)
        if response_client.status_code == 200:
            data_name = response_client.text
            client_name = data_name
        else:
            client_name = "No encontrado"
            print(f"Error: {response_client.status_code}")

        config = {
            "rut": rut,
            "year": year,
            "ipc": ipc,
            "custom": custom,
            "drive_id": drive_id,
            "client_name": client_name
        }

        print("config:", config)

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
