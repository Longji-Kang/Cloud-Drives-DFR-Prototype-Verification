from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

import os

KEY_VAULT_NAME = os.environ['KEY_VAULT_NAME']
KEY_VAULT_URI  = f'https://{KEY_VAULT_NAME}.vault.azure.net'
AES_MODE       = AES.MODE_EAX

def decrypt_file_name(name: str):
    # Get Key Vault key
    creds = ManagedIdentityCredential(
        client_id = os.environ['MANAGED_CLIENT_ID']
    )

    client = SecretClient(
        vault_url  = KEY_VAULT_URI,
        credential = creds
    )

    hex = client.get_secret(os.environ['DB_SECRET_NAME']).value

    key_bytes = bytes.fromhex(hex)

    # Separate name parts
    tag_hex = name[0:32]
    nonce_hex = name[32:64]
    name_hex = name[64:]

    tag_bytes = bytes.fromhex(tag_hex)
    nonce_bytes = bytes.fromhex(nonce_hex)
    name_bytes = bytes.fromhex(name_hex)

    # Decrypt file name
    cipher = AES.new(
        key = key_bytes,
        mode = AES_MODE,
        nonce = nonce_bytes
    )

    data = cipher.decrypt_and_verify(name_bytes, tag_bytes)

    return data.decode('utf-8')