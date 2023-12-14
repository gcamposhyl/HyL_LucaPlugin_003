from firebase_functions import https_fn

@https_fn.on_request(max_instances=10)
def test_moderator(req: https_fn.Request) -> https_fn.Response:
    from google.cloud import pubsub_v1
    import json
    import os
    project_id =  os.environ.get('PROJECT_ID_FIREBASE')
    topic_name = "ddjj"
    publisher = pubsub_v1.PublisherClient()
    
    try:
        output = {
            'messageId': '1702562205193',
            'pluginId': 'hLBRSK18Xxge',
            'recipient': 'hLBRSK18Xxge',
            'inputCheckbox': '["1948"]',
            'inputText': '["13.687.886-7","2022"]',
            'region': 'us-central1',
            'status': 'procesando',
            'name': 'ddjj',
            'projectName': 'lucaplugs-dev',
            'outputMessage': '',
            'sender':'Core',
            'userId': 'sF6Z07wuSkQN95E64EYFYUrIJul1',
            'cardId': 'W4Z44N9N',
            'outputFile': {'1948': ''},
            'email': 'asalazar@hyl.cl',
            'inputFiles': '[]',
            'timestamp': '12/14/2023 10:56:45'
        }
        message_json = json.dumps(output)
        message_bytes = message_json.encode('utf-8')
        topic_path = publisher.topic_path(project_id, topic_name)
        future = publisher.publish(topic_path, message_bytes)
        future.result() 
        return https_fn.Response(f"Mensaje publicado en el tema de Pub/Sub: {topic_name}", status=200, mimetype="application/json")
    
    except Exception as ex:
        print(str(ex))
        return https_fn.Response("test_ddjj started ...", status=200, mimetype="application/json")