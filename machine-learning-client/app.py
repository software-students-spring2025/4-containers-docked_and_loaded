"""Flask"""

import traceback
from flask import Flask, request, jsonify
from classify import classify_rps_base64


app = Flask(__name__)


@app.route("/classify", methods=["POST"])
def classify():
    """
    classify
    """
    data = request.get_json()
    image_base64 = data.get("image")

    if not image_base64:
        print("No image provided")
        return jsonify({"error": "No image provided"}), 400

    print("📸 Received image (first 100 chars):", image_base64[:100])

    try:
        move = classify_rps_base64(image_base64)
        print("MLC classified:", move)
        return jsonify({"move": move})
    except ValueError as e:
        print("MLC error:", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
