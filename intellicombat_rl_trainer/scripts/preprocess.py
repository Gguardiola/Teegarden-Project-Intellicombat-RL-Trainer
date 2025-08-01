import os
import sys
import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

SIMULATED_LOGS_DIR = "../intellicombat_training_logs_manager/training_simulated_logs"
OUTPUT_FILE = "model/preprocessed_data.json"

MONGO_URI = "mongodb://mongodb:27017"
MONGO_DB = "intellicombat"
MONGO_COLLECTION = "combat_logs"

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.mappings import build_action_maps

def load_simulated_logs(directory_path, source_label):
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
                                entry["source"] = source_label
                                data.append(entry)
                    else:
                        content = json.load(f)
                        if isinstance(content, list):
                            for entry in content:
                                entry["source"] = source_label
                                data.append(entry)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    return data

async def load_real_logs_from_mongo():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]

    cursor = collection.find({})
    logs = []
    async for doc in cursor:
        doc.pop("_id", None)
        doc["source"] = "real"
        logs.append(doc)

    return logs

async def preprocess():
    print("Loading real logs from MongoDB...")
    real_data = await load_real_logs_from_mongo()

    print("Loading simulated logs from disk...")
    simulated_data = load_simulated_logs(SIMULATED_LOGS_DIR, "simulated")

    if not real_data:
        print("Real logs not found! Using ONLY simulated ones...")
        all_data = simulated_data
    else:
        all_data = real_data + simulated_data

    print(f"Total entries: {len(all_data)} (real: {len(real_data)}, simulated: {len(simulated_data)})")

    with open(OUTPUT_FILE, "w") as out:
        json.dump(all_data, out, indent=2)

    print(f"Preprocess done successfully, stored at {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(preprocess())
