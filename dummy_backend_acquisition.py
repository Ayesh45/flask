import sys
import json
import os

input_json = sys.stdin.read()
data = json.loads(input_json)

# Simulate saving a CSV
os.makedirs("uploads", exist_ok=True)
file_path = os.path.join("uploads", "acquired_data.csv")
with open(file_path, "w") as f:
    f.write("Name,Age,Dept\nAlice,25,HR\nBob,30,IT\nCarol,28,Finance\nDave,35,IT\nEve,29,HR\n")

# Sample preview data (first 5 rows)
sample_data = [
    {"Name": "Alice", "Age": 25, "Dept": "HR"},
    {"Name": "Bob", "Age": 30, "Dept": "IT"},
    {"Name": "Carol", "Age": 28, "Dept": "Finance"},
    {"Name": "Dave", "Age": 35, "Dept": "IT"},
    {"Name": "Eve", "Age": 29, "Dept": "HR"}
]

output = {
    "status": "success",
    "file_path": file_path,
    "sample_data": sample_data
}

print(json.dumps(output))
