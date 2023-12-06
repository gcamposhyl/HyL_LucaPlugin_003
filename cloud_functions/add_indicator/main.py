import firebase_admin
from firebase_admin import firestore
from flask import escape
from firebase_functions import https_fn

# Application Default credentials are automatically created.
app = firebase_admin.initialize_app()
db = firestore.client()

@https_fn.on_request(max_instances=10)
def plugin_v1_ddjj1948_add_indicator(req: https_fn.Request) -> https_fn.Response:
    """HTTP Cloud Function.
    """
    indicator_json = req.get_json(silent=True)
    
    if indicator_json is None:
        print("No se pudo decodificar el mensaje recibido")
        return "Error decoding JSON", 400
    
    collection = indicator_json["indicator"]
    document = indicator_json["document"]
    data = indicator_json["data"]

    doc_ref = db.collection("ddjj").document("indicators").collection(collection)
    new_doc_ref = doc_ref.document(document).set(data)


    return f"Indicador {collection} agregado"
