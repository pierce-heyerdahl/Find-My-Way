from flask import Flask
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__, static_folder = '../frontend/build/', static_url_path = '/')
CORS(app)

@app.route("/test")
@cross_origin()
def numbers():
    return {"numbers": ["One", "Two"]}

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True, port = int(os.environ.get("PORT", 5000)))
