from flask import Flask, render_template, request
import json
import subprocess
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

session_data = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat/<process_name>")
def chat(process_name):
    if process_name == "data_preprocessing":
        session_data.clear()
        session_data["steps"] = []
    return render_template("chatbot.html", process_name=process_name, stage="start")

@app.route("/submit/<process_name>", methods=["POST"])
def submit(process_name):
    global session_data
    if process_name == "data_preprocessing":
        stage = request.form.get("stage")

        if stage == "start":
            file_path = request.form.get("csv_path")
            session_data["file_path"] = file_path
            return render_template("chatbot.html",
                                   process_name=process_name,
                                   stage="target_column",
                                   filepath=file_path)

        elif stage == "target_column":
            target_column = request.form.get("target_column")
            session_data["target_column"] = target_column
            return render_template("chatbot.html",
                                   process_name=process_name,
                                   stage="preprocessing_steps",
                                   target_column=target_column)

        elif stage == "preprocessing_steps":
            step = request.form.get("preprocess_step").strip()
            if step.lower() != "no":
                session_data["steps"].append(step)
                return render_template("chatbot.html",
                                       process_name=process_name,
                                       stage="preprocessing_steps",
                                       last_step=step)
            else:
                # Call preprocessing backend
                try:
                    backend_input = {
                        "file_path": session_data.get("file_path"),
                        "target_column": session_data.get("target_column"),
                        "steps": session_data.get("steps")
                    }
                    result = subprocess.run(
                        ["python", "dummy_backend.py"],
                        input=json.dumps(backend_input),
                        text=True,
                        capture_output=True,
                        check=True
                    )
                    backend_output = json.loads(result.stdout)
                except:
                    backend_output = {"status": "error", "message": "Backend error"}

                return render_template("chatbot.html",
                                       process_name=process_name,
                                       stage="finished",
                                       backend_output=json.dumps(backend_output, indent=4))

    elif process_name == "data_acquisition":
        user_input = request.form.get("user_input", "")

        # Call acquisition backend (sample JSON)
        try:
            backend_input = {"request": user_input}
            result = subprocess.run(
                ["python", "dummy_backend_acquisition.py"],
                input=json.dumps(backend_input),
                text=True,
                capture_output=True,
                check=True
            )
            backend_output = json.loads(result.stdout)
        except:
            backend_output = {"status": "error", "message": "Backend error"}

        return render_template("chatbot.html",
                               process_name=process_name,
                               stage="finished",
                               backend_output=json.dumps(backend_output, indent=4),
                               sample_data=backend_output.get("sample_data"))

    else:
        return "Unknown process", 400

if __name__ == "__main__":
    app.run(debug=True)
