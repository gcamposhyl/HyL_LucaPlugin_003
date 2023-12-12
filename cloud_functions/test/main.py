from firebase_functions import https_fn

@https_fn.on_request(max_instances=10)
def test_orderer_data(req: https_fn.Request) -> https_fn.Response:
    import pandas as pd
    import json
    import os
    from components.utils.data_service import Data_manipulation

    try:
        connection_drive = Data_manipulation()
        if req.method == 'POST':
            request_data = req.get_json()
            full_data = json.dumps(request_data, indent=2)

            for dicc in request_data:
                return None

    except Exception as ex:
        print(str(ex))

    return https_fn.Response("Función iniciada...", status=200, mimetype="application/json")