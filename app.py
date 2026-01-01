from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pytubefix import YouTube
import os

app = Flask(__name__)
CORS(app)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/api/video-info", methods=["POST"])
def video_info():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL required"}), 400

    yt = YouTube(url)
    return jsonify({
        "title": yt.title,
        "views": yt.views,
        "length": yt.length,
        "thumbnail": yt.thumbnail_url
    })

@app.route("/api/download", methods=["POST"])
def download_video():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL required"}), 400

    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension="mp4") \
                       .order_by("resolution").desc().first()
    if not stream:
        return jsonify({"error": "No stream found"}), 500

    file_path = stream.download(output_path=DOWNLOAD_FOLDER)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run()