#!/bin/bash
echo "==============================================="
echo "====      INTELLICOMBAT MODEL TRAINER     ====="
echo "==============================================="
echo ""
echo "- Before starting:"
echo "-- Remember to populate the /training_simulated_logs or /training_converted_real_logs folders in order to train and create a consistent AI model."


set -e 

echo "Preprocessing data..."
python3 scripts/preprocess.py

echo "Training the model..."
python3 scripts/train_model.py

echo "Exporting to ONNX..."
python3 scripts/export_model.py

echo "ALL DONE!!"
