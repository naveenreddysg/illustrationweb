from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("helloanalytics.html")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="localhost", debug=True, port=port)