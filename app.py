import vsm
import route
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)



@app.route('/')
def index():
    return "Hello, World"


app.add_url_rule('/c', view_func=vsm.main)
app.add_url_rule('/query/<query>', view_func=route.queryType)



app.add_url_rule('/d', view_func=route.d)
app.add_url_rule('/p', view_func=route.p)



if __name__ == "__main__":
    app.run(debug=True)