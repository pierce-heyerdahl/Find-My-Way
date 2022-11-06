from flask import Flask
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory
import os

app = Flask(__name__, static_folder = '../frontend/build/', static_url_path = '/')
CORS(app)

@app.route("/test", methods=['GET'])
@cross_origin()
def numbers():
    return {"numbers": ["four", "five"]}

@app.route("/")
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    #app.run(host = "0.0.0.0", debug = True, port = int(os.environ.get("PORT", 5000)))
    app.run()
