import os
import base64
from flask import Flask, request
from process_video import process_video

app = Flask(__name__)


# if __name__ == '__main__':
#     process_video(sys.argv[1], sys.argv[2])

@app.route("/", methods=["POST"])
def index():
    """Receive and parse Pub/Sub messages."""
    envelope = request.get_json()
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]

    name = "World"
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        video = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()
        print(video)
        parts_video = video.split("\n")
        print(parts_video[0])
        print(parts_video[1])
        process_video(int(parts_video[0]), parts_video[1])

    print(f"Processed video!")

    return ("", 204)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
