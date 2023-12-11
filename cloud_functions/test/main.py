from firebase_functions import https_fn

@https_fn.on_request(max_instances=10)
def test_moderator(req: https_fn.Request) -> https_fn.Response:
    import json
    import os
    from google.cloud import pubsub_v1

    project_id =  os.environ.get('PROJECT_ID_FIREBASE')
    topic_name = "ddjj"
    publisher = pubsub_v1.PublisherClient()

    try:
        output = {
            "name": "ddjj",
            "inputCheckbox": ["1948"],
            "pluginId": "7efgvs89HwR",
            "messageId": "52156748954256",
            "cardId": "B45VHfdAS0",
            "userId": "kjahdiekgSlhdkcaliSDJHJ",
            "inputFiles": "[]",
            "inputText": '[{"ddjj":"1948", "rut":"76042734-9", "year":"2023"}]',
        }

        message_json = json.dumps(output)
        message_bytes = message_json.encode('utf-8')
        topic_path = publisher.topic_path(project_id, topic_name)
        future = publisher.publish(topic_path, message_bytes)
        future.result() 
        print("Mensaje publicado en el tema de Pub/Sub:", topic_name)

    except Exception as ex:
        print(str(ex))
    return https_fn.Response("test_ddjj started ...", status=200, mimetype="application/json")
