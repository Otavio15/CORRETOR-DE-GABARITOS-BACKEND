import json
import os
import time

from flask import Flask, request

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = "/home/otavio/Desktop"


@app.route("/resultado", methods=['GET', 'POST'])
def index():
    return json.load(open("dados.json"))


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if request.files:
            image = request.files["image"]
            image.save(os.path.join(
                app.config["IMAGE_UPLOADS"], image.filename))
            import segmentacao
            return json.load(open("dados.json"))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
