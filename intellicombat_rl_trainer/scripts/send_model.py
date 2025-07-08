from minio import Minio
from minio.error import S3Error

client = Minio(
    "minio-bucket:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

bucket_name = "models"
found = client.bucket_exists(bucket_name)
if not found:
    client.make_bucket(bucket_name)
    print(f"bucket created: {bucket_name}")
else:
    print(f"Bucket {bucket_name} already exists.")

client.fput_object(
    bucket_name,         
    "intellicombat_model_ready.onnx",
    "../model/intellicombat_model_ready.onnx"
)