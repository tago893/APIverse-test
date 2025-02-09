"""
APIverse: A Flask app for API key management with Google OAuth.
"""

import flask
import os
from index import Index
from callback import Callback
from logout import Logout
from dashboard import Dashboard, GenerateKey  # Import GenerateKey
from login import Login  # Import Login class
app = flask.Flask(__name__)       # our Flask app
app.secret_key = os.urandom(24)



app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

app.add_url_rule('/login',
                 view_func=Login.as_view('login'),
                 methods=["GET"])
app.add_url_rule('/callback',
                 view_func=Callback.as_view('callback'),
                 methods=["GET"])


app.add_url_rule('/dashboard',
                 view_func=Dashboard.as_view('dashboard'),
                 methods=["GET", "POST"])

app.add_url_rule('/generate-key',
                 view_func=GenerateKey.as_view('generate_key'),
                 methods=["POST"])  

app.add_url_rule('/logout',
                 view_func=Logout.as_view('logout'),
                 methods=["GET"])
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
