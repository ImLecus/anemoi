from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import json
from openaq import OpenAQ
import threading
from pathlib import Path

load_dotenv()

API_URL = "https://api.openaq.org/v3/locations"
API_KEY = os.environ["API_KEY"]
DATA_FILE = Path("data/data.json")
FETCH_INTERVAL_SECONDS = 3600
PORT = 5000

app = Flask(__name__)
Path("data").mkdir(parents=True, exist_ok=True)

cache = {"meta": {}, "results": []}

def fetch(stop_event):
    """
        Periodically fetches the OpenAQ API and stores the result

        When the stop_event is set (outside the function), this function closes the client
        and ends
    """
    global cache
    client = OpenAQ(api_key=API_KEY)
    try:
        while not stop_event.is_set():
            try:
                cache = client.locations.list(parameters_id=2, limit=1000)
            except Exception as e:
                print(e)
            stop_event.wait(FETCH_INTERVAL_SECONDS)
    finally:
        client.close()


@app.route("/api/health", methods=["GET"])
def health():
    """Simple endpoint to prove the API lives"""
    return jsonify({"status": "ok"})

@app.route("/api/locations", methods=["GET"])
def get_locations():
    """Retuns all the locations"""
    return cache.json()


def main():
    """
        Invokes a thread that fetches the OpenAQ API and exposes a REST API to the frontend
    """
    stop_event = threading.Event()
    fetch_thread = threading.Thread(target=fetch, args=(stop_event,), daemon=True)
    fetch_thread.start()

    from waitress import serve
    print(f"Server listening on port {PORT}.\nPress Ctrl+C to stop it.")
    serve(app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()