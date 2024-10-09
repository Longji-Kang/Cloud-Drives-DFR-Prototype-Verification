from pymongo import MongoClient

import os

def get_collection():
    CONN            = os.environ['CUSTOMCONNSTR_EvidenceStoreConnectionString']
    COLLECTION_NAME = os.environ['EVIDENCE_DB_COLLECTION']
    DB_NAME         = os.environ["MONGO_DB_NAME"]

    client = MongoClient(CONN)

    db         = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    return collection

def get_e_hash(file_name: str) -> str:
    collection = get_collection()

    query_obj = {
        "evidence_file_id": file_name
    }

    result = collection.find_one(query_obj)

    return result['e_hash']

def set_verified_status(file_name: str, status: bool):
    collection = get_collection()

    verification_status = 'Verified' if status == True else 'Verification failed!'

    query_obj = {
        "evidence_file_id": file_name
    }

    update_obj = {
        "$set": {
            "verfication_status": verification_status
        }
    }

    collection.update_one(
        query_obj,
        update_obj
    )