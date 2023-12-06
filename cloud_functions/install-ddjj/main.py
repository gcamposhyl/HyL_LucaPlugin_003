from firebase_functions import https_fn

@https_fn.on_request(max_instances=10)
def plugin_v1_install_serbimas_egresos(req: https_fn.Request) -> https_fn.Response:
    print("manejar test de info")
    return https_fn.Response("ok")