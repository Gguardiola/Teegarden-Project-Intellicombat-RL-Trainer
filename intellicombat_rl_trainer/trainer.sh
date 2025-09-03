#!/bin/bash
echo "==============================================="
echo "====      INTELLICOMBAT MODEL TRAINER     ====="
echo "==============================================="
echo ""

. /etc/environment
set -e

cd /code/app/intellicombat_rl_trainer

PYTHON="/usr/local/bin/python3"

echo "Using Python: $PYTHON"

echo "Preprocessing data..."
$PYTHON scripts/preprocess.py

echo "Training the model..."
$PYTHON scripts/train_model.py

echo "Exporting to ONNX..."
$PYTHON scripts/export_model.py

echo "Sending to S3(MINIO)..."
$PYTHON scripts/send_model.py

echo "ALL DONE!!"
