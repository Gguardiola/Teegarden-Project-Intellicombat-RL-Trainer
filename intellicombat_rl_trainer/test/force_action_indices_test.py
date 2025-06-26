import numpy as np
from tensorflow.keras.models import load_model
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.mappings import build_action_maps

model = load_model("../model/intellicombat_model.keras")

with open("../model/preprocessed_data.json", "r") as f:
    data = json.load(f)

_, index_to_action = build_action_maps(data)
num_actions = len(index_to_action)

print("Index prediction by force...")
for forced_index in range(num_actions):
    fake_output = np.zeros((1, num_actions), dtype=np.float32)
    fake_output[0][forced_index] = 9999

    dummy_input = np.array([[50, 50, 0, 50, 50, 0]], dtype=np.float32)
    pred = model.predict(dummy_input, verbose=0)

    pred[0] = fake_output[0]

    predicted_index = int(np.argmax(pred))
    predicted_action = index_to_action[predicted_index]

    print(f"[{forced_index}] Force index prediction: {predicted_index} -> action: {predicted_action}")
