import firebase_admin
from firebase_admin import firestore, credentials
from firebase_functions import https_fn

cred = credentials.Certificate('config/lucaplugs-sa.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()


@https_fn.on_request(max_instances=10)
def core_v1_add_indicator(req: https_fn.Request) -> https_fn.Response:
    """HTTP Cloud Function.
    """
    try:
        indicator_json = req.get_json(silent=True)
        
        if indicator_json is None:
            print("No se pudo decodificar el mensaje recibido")
            return "Error decoding JSON", 400
        
        collection = indicator_json["indicator"]
        document = indicator_json["document"]
        data = indicator_json["data"]

        doc_ref = db.collection(collection).document(document)
        doc_ref.set(data)


        return f"Indicador {collection} agregado"
    except Exception as e:
        print("Error:", str(e))
        return f"Error interno del servidor: {str(e)}", 500
