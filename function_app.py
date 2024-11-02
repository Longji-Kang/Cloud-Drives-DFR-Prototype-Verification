import azure.functions as func
import db_processor as db
import blob_processor as blob_inter
import encryption as enc
import hashlib

import logging

import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

LOGGING_PREFIX = "[DFR Prototype] - "

@app.function_name("evidence_verification")
@app.route("")
def main(req: func.HttpRequest) -> func.HttpResponse:
    data_string = req.get_body().decode()
    json_obj    = json.loads(data_string)
    
    logging.info(f"{LOGGING_PREFIX}Verifying evidence file {json_obj['evidence_file_name']}")
    evidence_name = enc.decrypt_file_name(json_obj["evidence_file_name"])

    logging.info(f"{LOGGING_PREFIX}Comparing encrypted evidence file hash")
    e_hash = db.get_e_hash(json_obj["evidence_file_name"])

    blob_content = blob_inter.get_current_blob_hash(evidence_name)
    
    new_hash = hashlib.md5(blob_content).hexdigest()

    if e_hash == new_hash:
        logging.info(f"{LOGGING_PREFIX}Evidence file verified")
        db.set_verified_status(json_obj["evidence_file_name"], True)
    else:
        logging.info(f"{LOGGING_PREFIX}Evidence file had issues during verification")
        db.set_verified_status(json_obj["evidence_file_name"], False)

    return func.HttpResponse(
        'success',
        status_code=200
    )