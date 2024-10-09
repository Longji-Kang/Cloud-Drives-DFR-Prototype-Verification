import azure.functions as func
import db_processor as db
import blob_processor as blob_inter
import encryption as enc
import hashlib

import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.function_name("evidence_verification")
@app.route("")
def main(req: func.HttpRequest) -> func.HttpResponse:
    data_string = req.get_body().decode()
    json_obj    = json.loads(data_string)

    evidence_name = enc.decrypt_file_name(json_obj["evidence_file_name"])

    e_hash = db.get_e_hash(json_obj["evidence_file_name"])

    blob_content = blob_inter.get_current_blob_hash(evidence_name)
    
    new_hash = hashlib.md5(blob_content).hexdigest()

    if e_hash == new_hash:
        db.set_verified_status(json_obj["evidence_file_name"], True)
    else:
        db.set_verified_status(json_obj["evidence_file_name"], False)

    return func.HttpResponse(
        'success',
        status_code=200
    )