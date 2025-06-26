import json
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.mappings import build_action_maps

PREPROCESSED_FILE = "model/preprocessed_data.json"
MODEL_OUTPUT_PATH = "model/intellicombat_model.keras"

REAL_SAMPLE_WEIGHT = 2.0
INPUT_FEATURES = [
    "actorHP", "actorEnergy", "actorShield",
    "opponentHP", "opponentEnergy", "opponentShield"
]

def encode_state(state):
    return [state.get(k, 0) for k in INPUT_FEATURES]

def load_data():
    with open(PREPROCESSED_FILE, "r") as f:
        data = json.load(f)

    states, actions, rewards, weights = [], [], [], []

    action_map, _ = build_action_maps(data)

    for entry in data:
        s = encode_state(entry["state"])
        a = action_map[entry["action"]]
        r = entry["reward"]
        w = REAL_SAMPLE_WEIGHT if entry.get("source") == "real" else 1.0

        states.append(s)
        actions.append(a)
        rewards.append(r)
        weights.append(w)

    states = np.array(states)
    actions = np.array(actions)
    rewards = np.array(rewards)
    weights = np.array(weights)

    return states, actions, rewards, weights, action_map

def create_model(input_dim, num_actions):
    inputs = layers.Input(shape=(input_dim,))
    x = layers.Dense(64, activation="relu")(inputs)
    x = layers.Dense(64, activation="relu")(x)
    outputs = layers.Dense(num_actions, activation="linear", name="output")(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs) 
    model.compile(optimizer="adam", loss="mse")
    return model

def train():
    print("Loading dataset...")
    states, actions, rewards, weights, action_map = load_data()
    num_actions = len(action_map)
    input_dim = states.shape[1]

    print(f"Training with {len(states)} states, {num_actions} actions available.")

    targets = np.zeros((len(states), num_actions))
    for i, (a, r) in enumerate(zip(actions, rewards)):
        targets[i, a] = r

    print("Creating model...")
    model = create_model(input_dim, num_actions)

    print("Training model...")
    model.fit(states, targets, sample_weight=weights, epochs=30, batch_size=32)

    print(f"Model stored at {MODEL_OUTPUT_PATH}")
    model.save(MODEL_OUTPUT_PATH)

    print("Training completed!")

if __name__ == "__main__":
    train()
