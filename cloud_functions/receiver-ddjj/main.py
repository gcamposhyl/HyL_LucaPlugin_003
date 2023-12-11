
from firebase_functions import https_fn, pubsub_fn


@pubsub_fn.on_message_published(max_instances=10, topic="ddjj1948")
def plugin_v1_ddjj_receiver(event: pubsub_fn.CloudEvent[pubsub_fn.MessagePublishedData]) -> None:
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
        print("data en receiver", data)

        #limpia memoria hasta este punto
        gc.collect()

    except Exception as e:
        print("Error en moderator:", str(e))
        return f"Error interno del servidor en moderator: {str(e)}", 500
