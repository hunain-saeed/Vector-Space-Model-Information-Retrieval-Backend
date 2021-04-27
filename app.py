import vsm
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "Hello, World"

app.add_url_rule('/h', view_func=vsm.hello_world)


if __name__ == "__main__":
    app.run(debug=True)