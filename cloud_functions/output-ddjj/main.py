from firebase_functions.firestore_fn import (
  on_document_updated,
  Event,
  Change,
  DocumentSnapshot,
)
from firebase_admin import firestore, credentials
import firebase_admin
import gc
import os
import json

@on_document_updated(max_instances=10, document="ddjj/{userId}/1948/{cardId}/tasks/{taskId}")
def plugin_v1_ddjj1948_output(event: Event[Change[DocumentSnapshot]]) -> None:
  try:
    # cred_path = os.path.abspath('config/lucaplugs-sa.json')
    # cred = credentials.Certificate(cred_path)
    cred = credentials.ApplicationDefault()
    db = firestore.client()

    value_modified = event.data.after.to_dict()
    print("value_modified", value_modified)
    user_id = event.params["userId"]
    card_id = event.params["cardId"]

    #* Obtención de datos desde firestore
    doc_deflactada = db.collection("ddjj").document(str(user_id)).collection("1948").document(str(card_id)).collection("tasks").document("deflactada")
    doc_estandar = db.collection("ddjj").document(str(user_id)).collection("1948").document(str(card_id)).collection("tasks").document("estandar")
    status_deflactada = doc_deflactada.get().to_dict()["status"]
    status_estandar = doc_estandar.get().to_dict()["status"]

    if status_deflactada == True & status_estandar == True:
      doc_config = db.collection("ddjj").document(str(user_id)).collection("1948").document(str(card_id)).collection("current_custom").document("config")
      doc_message = db.collection("ddjj").document(str(user_id)).collection("1948").document(str(card_id)).collection("current_custom").document("message")
      drive_id = doc_config.get().to_dict()["drive_id"]
      message = doc_message.get().to_dict()
      url_folder_drive = f'https://drive.google.com/drive/folders/{drive_id}'

      #* Construcción de mensaje de output
      message = {
        "status": "ok",  
        "plugin_name": message["plugin_name"],
        "plugin_id": message["plugin_id"],
        "message_id": message["message_id"], 
        "card_id": card_id,
        "user_id": user_id,
        "input_text": message["input_text"],
        "current_task": "1948",
        "config": doc_config.get().to_dict(),
        "output": url_folder_drive
      }

      #* Descomentar al final!
      topic = 'plugin-output-message'
      json_data = json.dumps(message)
      data_bytes = json_data.encode('utf-8')
      project_id = os.environ.get('PROJECT_ID_FIREBASE')
      topic_published = publisher_topic(data_bytes, project_id, topic)
      print("Estado de publicación de tópico:",topic_published)

      #limpia memoria hasta este punto
      gc.collect()
      print("El proceso DJ1948 se encuentra completado")

    else:
      print("El proceso DJ1948 aun no se completa")

  except Exception as ex:
      print(f'error:{str(ex)}')
      return {"res": str(ex)}

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