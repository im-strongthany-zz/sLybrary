from flask import Flask
app = Flask(__name__)

# connects to server
@app.route("/")
def index():
    if __name__ == "__main__":
        app.run(host='0.0.0.0', debug=True)
