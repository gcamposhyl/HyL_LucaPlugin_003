
from firebase_functions import https_fn, pubsub_fn


@pubsub_fn.on_message_published(max_instances=10, topic="ddjj")
def plugin_v1_ddjj_moderator(event: pubsub_fn.CloudEvent[pubsub_fn.MessagePublishedData]) -> None:
    """Pub/Sub Cloud Function.
    """
    from components.utils.resources import Cloud_elements
    from components.utils.resources import Firestore_resources

    try:
        import json
        import gc
        import os
        import traceback
        cloud_resources = Cloud_elements()
        firestore_resources = Firestore_resources()
    
        data = event.data.message.json

        input_text = data["inputText"]
        plugin_name = data["name"]
        print("plugin_name:", plugin_name)    
        card_id = data["cardId"]
        print("card_id:", card_id)
        user_id = data["userId"]
        print("user_id:", user_id)
        number_ddjj = data["inputCheckbox"][0]
        print("number_ddjj:", number_ddjj)

        # Convertir el string corregido a una lista
        string_files = input_text.replace("'", '"')
        data_list = json.loads(string_files)

        data_list_content = data_list[0]
        rut = data_list_content["rut"]
        print("rut:", rut)
        year = data_list_content["year"]
        print("year:", year)
        
        plugin_ddjj = f'{plugin_name}{number_ddjj}'
        print("plugin_ddjj:", plugin_ddjj)

        id_folder_drive = cloud_resources.obtain_folder_id(plugin_ddjj, user_id, card_id)

        message = {
            "plugin_name": plugin_name,
            "number_ddjj": number_ddjj,
            "plugin_id": data["pluginId"],
            "message_id": data["messageId"],
            "card_id": card_id,
            "user_id": user_id,
            "input_text": data["inputText"],
        }

        firestore_resources.create_custom(plugin_name, user_id, number_ddjj, card_id, message)


        
    except Exception as e:
        print("Error:", str(e))
        return f"Error interno del servidor: {str(e)}", 500

def publisher_topic(message, project_id, topic):
    from google.cloud import pubsub_v1
    publisher = pubsub_v1.PublisherClient()
    try:
        topic_path = publisher.topic_path(project_id, topic)
        future = publisher.publish(topic_path, message)
        topic_published = future.result()
        return topic_published
    except Exception as ex:
        print(f'error:{str(ex)}')
        return {"res": str(ex)}

