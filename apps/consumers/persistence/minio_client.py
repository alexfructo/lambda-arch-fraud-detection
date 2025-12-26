from minio import Minio

def create_minio_client(endpoint, access_key, secret_key):
    return Minio(
        endpoint.replace("http://", ""),
        access_key=access_key,
        secret_key=secret_key,
        secure=False
    )
