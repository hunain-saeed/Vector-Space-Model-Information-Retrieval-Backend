import vsm
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "Hello, World"

app.add_url_rule('/d', view_func=vsm.d)
app.add_url_rule('/p', view_func=vsm.p)
app.add_url_rule('/t', view_func=vsm.t)

if __name__ == "__main__":
    app.run(debug=True)