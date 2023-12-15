
from firebase_functions import https_fn, pubsub_fn


@pubsub_fn.on_message_published(max_instances=10, topic="exception_ddjj")
def plugin_v1_ddjj_exceptions(event: pubsub_fn.CloudEvent[pubsub_fn.MessagePublishedData]) -> None:
    """Pub/Sub Cloud Function.
    """
    try:  
        import json
        import gc
        import os
    
        data = event.data.message.json
        message = {
            "status": "ok",  
            "plugin_name": data["plugin_name"],
            "plugin_id": data["plugin_id"],
            "message_id": data["message_id"], 
            "card_id": data["card_id"],
            "user_id": data["user_id"],
            "input_text": data["input_text"],
            "current_task": "1948",
            "output": data["output"]
        }
        print("message:", message)
        print("Cloud function de excepción")
        #* Descomentar al final!
        # topic = 'plugin-output-message'
        # json_data = json.dumps(message)
        # data_bytes = json_data.encode('utf-8')
        # project_id = os.environ.get('PROJECT_ID_FIREBASE')
        # topic_published = publisher_topic(data_bytes, project_id, topic)
        # print("Estado de publicación de tópico:",topic_published)
        #limpia memoria hasta este punto
        gc.collect()
        
    except Exception as e:
        print("Error en moderator:", str(e))
        return f"Error interno del servidor en moderator: {str(e)}", 500

def publisher_topic(message, project_id, topic):
    from google.cloud import pubsub_v1
    publisher = pubsub_v1.PublisherClient()
    try:
        topic_path = publisher.topic_path(project_id, topic)
        future = publisher.publish(topic_path, message)
        topic_published = future.result()
        return topic_published
    except Exception as ex:
        print(f'error en publisher topic:{str(ex)}')
        return {"res": str(ex)}

