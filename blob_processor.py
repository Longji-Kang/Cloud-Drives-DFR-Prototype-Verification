from azure.storage.blob import BlobClient

import os

CONNECTION_STRING = os.environ["CUSTOMCONNSTR_BlobStorageConnectionString"]
CONTAINER_NAME    = os.environ["BLOB_CONTAINER_NAME"]

def get_current_blob_hash(file_name: str) -> str:
    client = BlobClient.from_connection_string(
        conn_str       = CONNECTION_STRING,
        container_name = CONTAINER_NAME,
        blob_name      = file_name
    )

    download_stream = client.download_blob()

    content_strings = download_stream.readall()
    
    return content_strings