#!/bin/bash
echo "==============================================="
echo "====      INTELLICOMBAT MODEL TRAINER     ====="
echo "==============================================="
echo ""
echo "- Before starting:"
echo "-- Remember to populate the /training_simulated_log folder and entries into MINIO collection in order to train and create a consistent AI model."

set -e

cd /code/app/intellicombat_rl_trainer
PYTHON=$(which python3)
echo "Preprocessing data..."
python3 scripts/preprocess.py

echo "Training the model..."
python3 scripts/train_model.py

echo "Exporting to ONNX..."
python3 scripts/export_model.py

echo "Sending to S3(MINIO)..."
python3 scripts/send_model.py

echo "ALL DONE!!"
