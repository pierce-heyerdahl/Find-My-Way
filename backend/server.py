from flask import Flask

app = Flask(__name__)

@app.route("/test")
def members():
    return {"numbers": ["One", "Two"]}

if __name__ == "__main__":
    app.run(debug = True)
