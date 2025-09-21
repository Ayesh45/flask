import json
import os

JSON_FILE = os.path.join(os.path.dirname(__file__), "data.json")

# Simple "hello" processing: read input, add a response field, write back
with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

data["response"] = f"Hello World! You entered: {data.get('user_input', '')}"

with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
