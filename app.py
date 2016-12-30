from flask import Flask
from flask import render_template

app = Flask(__name__, static_folder='data')


@app.route("/")
def index():
    return render_template("index.html", data_file='IBM.csv')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000, debug=True)
