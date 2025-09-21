import sys
import json
import time
import os

try:
    # Read JSON input from stdin
    input_json = sys.stdin.read()
    data = json.loads(input_json)

    # Simulate processing delay (so spinner is visible)
    time.sleep(1.5)

    file_path = data.get("file_path")
    steps = data.get("steps", [])
    target_column = data.get("target_column")

    # Check if file exists (for demo, just simulate)
    if not file_path or not os.path.exists(file_path):
        output = {
            "status": "error",
            "message": f"CSV file not found at path: {file_path}"
        }
    else:
        # Simulate creating preprocessed file
        os.makedirs("uploads", exist_ok=True)
        preprocessed_file = os.path.join("uploads", "preprocessed.csv")
        with open(preprocessed_file, "w") as f:
            f.write("column1,column2,column3\n")  # dummy CSV

        output = {
            "status": "success",
            "preprocessed_file": preprocessed_file,
            "target_column": target_column,
            "steps_applied": steps
        }

except Exception as e:
    output = {
        "status": "error",
        "message": str(e)
    }

# Return JSON to stdout
print(json.dumps(output))
