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

dummy_state = {
    "actorHP": 70.0,
    "actorEnergy": 30.0,
    "actorShield": 1,
    "opponentHP": 40.0,
    "opponentEnergy": 80.0,
    "opponentShield": 0
}

input_vector = np.array([[ 
    dummy_state["actorHP"],
    dummy_state["actorEnergy"],
    dummy_state["actorShield"],
    dummy_state["opponentHP"],
    dummy_state["opponentEnergy"],
    dummy_state["opponentShield"]
]], dtype=np.float32)

pred = model.predict(input_vector, verbose=0)

action_index = int(np.argmax(pred))
action_name = index_to_action[action_index]

print(f"Prediction: index {action_index} -> action '{action_name}'")
print("Q-values:", pred[0])
