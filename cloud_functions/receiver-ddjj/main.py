
from firebase_functions import https_fn, pubsub_fn


@pubsub_fn.on_message_published(max_instances=10, topic="ddjj1948")
def plugin_v1_ddjj1948_receiver(event: pubsub_fn.CloudEvent[pubsub_fn.MessagePublishedData]) -> None:
    """Pub/Sub Cloud Function.
    """
    from components.utils.resources import Firebase_resources
    from components.utils.resources import Cloud_elements
    from google.cloud import pubsub_v1
    try:
        import requests
        import json
        import os
        import gc
        publisher = pubsub_v1.PublisherClient()

        firebase_resources = Firebase_resources()
        cloud_elements = Cloud_elements()
        print("marca 01")
        data = event.data.message.json
        drive_id = data["drive_id"]
        
        card_id = data["card_id"]
        user_id = data["user_id"]
        region = data["region"]
        project_id = data["project_id"]
        print("marca 02")

        project_id_core = os.environ.get("PROJECT_ID_CORE")
        request_client_info = f"https://{region}-{project_id_core}.cloudfunctions.net/core-v1-get_data_interface/getClientByRut"
        request_client_data = f"https://{region}-{project_id_core}.cloudfunctions.net/core-v1-get_data_interface/getDdjjByRutAndYear"
        request_ipc = f'https://{region}-{project_id_core}.cloudfunctions.net/core-v1-get_data_interface/getAllByYear'
        
        print("marca 03")
        #* Obtener rut y año de cadena   
        input_text = data["input_text"]
        string_files = input_text.replace("'", '"')
        input_text_list = json.loads(string_files)

        #* Obtención de RUT y validaciones
        rut = str(input_text_list[0])
        rut_without_points = cloud_elements.rut_without_points(rut)
        rut_formatted = cloud_elements.formatted_rut(rut_without_points)

        #* Obtención de año y validaciones
        year = str(input_text_list[1])
        year_validated = cloud_elements.validate_year(year)

        params_ipc = {"year": year_validated}
        params_client = {"rut": rut_without_points}
        initial_data = {
            "year": int(year_validated),
            "rut": rut_formatted
        }
        print("marca 04")
        #* Solicitar IPC
        ipc = {}
        response_ipc = requests.get(request_ipc, params=params_ipc)
        if response_ipc.status_code == 200:
            data_ipc = response_ipc.json()
            ipc = data_ipc["ipc"]
        else:
            data_ipc = response_ipc.json()
            ipc = data_ipc["error"]
            print(f"Error: {response_ipc.status_code}")
        print("marca 05")

        #* Solicitar nombre de cliente
        client_name = ""
        response_client = requests.get(request_client_info, params=params_client)
        if response_client.status_code == 200:
            client_info = response_client.json()
            if not client_info:
                print("Rut ingresado no existe en DB")
                raise ValueError("El RUT ingresado no existe en el sistema")
            client_name = client_info["nombre"]
        else:
            client_name = "No encontrado"
            print(f"Error: {response_client.status_code}")

        print("marca 06")
        #* Solicitar data de cliente
        client_data = []
        response_data = requests.post(request_client_data, json=initial_data)
        if response_data.status_code == 200:
            data_client = response_data.json()
            client_data = data_client
            if client_data == []:
                print("Rut ingresado no existe en DB")
                raise ValueError("El rut ingresado no existe en el sistema")
        else:
            client_data = "No encontrado"
            print(f"Error: {response_data.status_code}")
         
        # Ordenar data
        orderer_data = cloud_elements.obtain_matrice(client_data)
        config_data = f"{orderer_data}"
        print("marca 07")
        config = {
            "rut": rut_formatted,
            "year": year_validated,
            "ipc": ipc,
            "custom": config_data,
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
    
    except ValueError as ve:
        print("Error en plugin_v1_ddjj1948_receiver:", str(ve))
        data["output"] = str(ve)
        message_json = json.dumps(data)
        message_bytes = message_json.encode('utf-8')
        topic_path = publisher.topic_path(project_id, "exception_ddjj")
        future = publisher.publish(topic_path, message_bytes)
        future.result() 
        return https_fn.Response(f"Error interno del servidor en moderator: {str(ve)}. Mensaje publicado en el tema de Pub/Sub: exception_ddjj", status=200, mimetype="application/json")

    except Exception as e:
        print("Error en plugin_v1_ddjj1948_receiver:", str(e))
        return f"Error interno del servidor en moderator: {str(e)}", 500
