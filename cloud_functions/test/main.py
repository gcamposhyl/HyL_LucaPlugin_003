from firebase_functions import https_fn

@https_fn.on_request(max_instances=10)
def plugin_v1_ddjj_obtain_matrice(req: https_fn.Request) -> https_fn.Response:
    import json
    from components.utils.data_service import Data_manipulation

    try:
        manipulation_data = Data_manipulation()
        if req.method == 'POST':
            request_data = req.get_json()
            matrice = manipulation_data.row_orderer(request_data)
            print("result:", matrice)
            matrice_json = json.dumps(matrice)
            return https_fn.Response(matrice_json, status=200, mimetype="application/json")
    except Exception as ex:
        print(str(ex))
        return https_fn.Response("Error al crear matriz", status=500, mimetype="application/json")