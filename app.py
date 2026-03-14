import subprocess
from flask import Flask, render_template, request

app = Flask(__name__)

PYTHON_EXEC = ".venv/bin/python"
SEGMENT_MODULE_PATH = "scripts.segment"

@app.route("/", methods=["GET", "POST"])
def index():
    image = None

    form_data = {
        "use_otsu": "true",
        "threshold": "0.5",
        "normalize": "true",
        "handle_nan": "true",
        "bins": "256",
        "angle": "0"
    }

    if request.method == "POST":
        form_data["use_otsu"] = "true" if request.form.get("use_otsu") else "false"
        form_data["threshold"] = request.form.get("threshold", "0.5")
        form_data["normalize"] = request.form.get("normalize", "true")
        form_data["handle_nan"] = request.form.get("handle_nan", "true")
        form_data["bins"] = request.form.get("bins", "256")
        form_data["angle"] = request.form.get("angle", "0")

        cmd = [
            PYTHON_EXEC,
            "-m", SEGMENT_MODULE_PATH,
            "--use_otsu", form_data["use_otsu"],
            "--threshold", form_data["threshold"],
            "--normalize", form_data["normalize"],
            "--handle_nan", form_data["handle_nan"],
            "--bins", form_data["bins"],
            "--angle", form_data["angle"],
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        image = result.stdout.strip()

    return render_template("index.html", image=image, form_data=form_data)

if __name__ == "__main__":
    app.run(debug=True)