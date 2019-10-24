import os

from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/resultado", methods=['GET','POST'])
def index():
    return json.load(open("dados.json"))

@app.route('/upload', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if request.files:

			print("OK")
			return json.load(open("dados.json"))

if __name__ == "__main__":
    app.run(host='0.0.0.0')