from minio import Minio
from config import *

def create_connection():

    client = Minio(
        MINIO_ENDPOINT,
        MINIO_ACCESS,
        MINIO_SECRET,
        secure=False
    )

    return client

def send_photo(client, path, img_name):
    client.fput_object('avatars', img_name, path)

def get_photo(client, path, img_name):
    client.fget_object('avatars', img_name, path)

def delete_photo(client, img_name):
    client.remove_object('avatars', img_name)