from flask import Flask

app = Flask(__name__)
@app.route("/")
def index():
    return "hi"

app.run(port=8080, host='0.0.0.0')