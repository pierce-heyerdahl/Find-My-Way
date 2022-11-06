from flask import Flask
import os

app = Flask(__name__, static_folder = '../frontend/build/', static_url_path = '/')

@app.route("/test")
def members():
    return {"numbers": ["One", "Two"]}

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True, port = int(os.environ.get("PORT", 5000)))
