from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory

import front_end_api_controller
import external_api_controller

app = Flask(__name__, static_folder = '../frontend/build/', static_url_path = '/')

app.register_blueprint(front_end_api_controller.bp)
app.register_blueprint(external_api_controller.bp)

CORS(app)

@app.route("/")
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/test", methods=['GET'])
@cross_origin()
def numbers():
    return {"numbers": ["four", "five"]}

if __name__ == "__main__":
    #app.run(host = "0.0.0.0", debug = True, port = int(os.environ.get("PORT", 5000)))
    app.run()