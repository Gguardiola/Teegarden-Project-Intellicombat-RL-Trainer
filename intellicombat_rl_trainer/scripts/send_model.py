import os
import glob
from minio import Minio
from minio.error import S3Error

client = Minio(
    "minio-bucket:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

BUCKET_NAME = "models"
MODEL_DIR = "../model"

files = glob.glob(os.path.join(MODEL_DIR, "intellicombat_model_ready_*.onnx"))
if not files:
    raise FileNotFoundError("No ONNX model found in local directory!")

model_path = files[0]
model_filename = os.path.basename(model_path)

print(f"Found: {model_filename}")

if not client.bucket_exists(BUCKET_NAME):
    client.make_bucket(BUCKET_NAME)
    print(f"Bucket '{BUCKET_NAME}' created")

try:
    client.fput_object(
        BUCKET_NAME,
        model_filename,
        model_path
    )
    print(f"Uploaded {model_filename} to MinIO")

    os.remove(model_path)
    print(f"Deleted local file {model_filename}")

except S3Error as e:
    print(f"Upload failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
