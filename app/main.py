from flask import Flask, render_template, Response, jsonify, request

from detector import (
    generate_frames,
    get_all_data
)

from ai_agent import ask_ai

app = Flask(__name__)


# ==========================================
# Home Page
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# Live Video Feed
# ==========================================

@app.route("/video_feed")
def video_feed():

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# ==========================================
# Dashboard API
# ==========================================

@app.route("/vehicle_count")
def vehicle_count():

    return jsonify(
        get_all_data()
    )


# ==========================================
# AI Chat
# ==========================================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    question = data.get("message", "")

    traffic = get_all_data()

    answer = ask_ai(question, traffic)

    return jsonify({
        "reply": answer
    })


# ==========================================
# Run Flask
# ==========================================

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False
    )