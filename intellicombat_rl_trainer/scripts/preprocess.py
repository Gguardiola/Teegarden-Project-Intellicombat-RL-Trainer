import os
import json
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.mappings import build_action_maps

REAL_LOGS_DIR = "../intellicombat_training_logs_manager/training_converted_real_logs"
SIMULATED_LOGS_DIR = "../intellicombat_training_logs_manager/training_simulated_logs"
OUTPUT_FILE = "model/preprocessed_data.json"

def load_logs_from_dir(directory_path, source_label):
    data = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".json") or filename.endswith(".jsonl"):
            full_path = os.path.join(directory_path, filename)
            try:
                with open(full_path, "r") as f:
                    if filename.endswith(".jsonl"):
                        for line in f:
                            if line.strip():
                                entry = json.loads(line)
                                if "source" not in entry:
                                    entry["source"] = source_label
                                data.append(entry)
                    else:
                        content = json.load(f)
                        if isinstance(content, list):
                            for entry in content:
                                if "source" not in entry:
                                    entry["source"] = source_label
                                data.append(entry)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    return data

def preprocess():
    print("Loading real logs...")
    real_data = load_logs_from_dir(REAL_LOGS_DIR, "real")

    print("Loading simulated logs...")
    simulated_data = load_logs_from_dir(SIMULATED_LOGS_DIR, "simulated")

    if not real_data:
        print("Real logs not found! Using ONLY simulated ones...")
        all_data = simulated_data
    else:
        all_data = real_data + simulated_data

    print(f"Total entries: {len(all_data)} (real: {len(real_data)}, simulated: {len(simulated_data)})")

    with open(OUTPUT_FILE, "w") as out:
        json.dump(all_data, out, indent=2)

    print(f"Prepocess donde successfuly, stored at {OUTPUT_FILE}")

if __name__ == "__main__":
    preprocess()
