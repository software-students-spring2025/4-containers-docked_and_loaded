"""
flask app
"""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    """
    route handler for the home page.
    """
    return "Hello"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
