"""
This is the main entry point for the Flask web application.
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello"

if __name__ == "__main__":
    """
    This route handles the homepage request and returns a simple greeting message.
    """
    app.run(host="0.0.0.0", port=5000)
