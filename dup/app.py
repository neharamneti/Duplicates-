from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        old_file = request.files["old_file"]
        new_file = request.files["new_file"]

        old_path = os.path.join(UPLOAD_FOLDER, old_file.filename)
        new_path = os.path.join(UPLOAD_FOLDER, new_file.filename)

        old_file.save(old_path)
        new_file.save(new_path)

        key_columns = ["ID"]   # change if needed

        # Read old scan keys only
        old_keys = pd.read_excel(old_path, usecols=key_columns, dtype=str)
        old_key_set = set(map(tuple, old_keys.values))

        # Read new scan
        new_df = pd.read_excel(new_path, dtype=str)

        # Filter new data
        mask = ~new_df[key_columns].apply(tuple, axis=1).isin(old_key_set)
        result_df = new_df[mask]

        output_path = os.path.join(UPLOAD_FOLDER, "filtered_new_scan.xlsx")
        result_df.to_excel(output_path, index=False)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
