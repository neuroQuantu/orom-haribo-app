"""Flask-SocketIO holographic dashboard for HARIBO dimension data."""

from __future__ import annotations

import importlib
import threading
import time
from typing import Any

flask = importlib.import_module("flask")
flask_socketio = importlib.import_module("flask_socketio")

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "haribo-orom-secret"
socketio = flask_socketio.SocketIO(app, cors_allowed_origins="*")
donnees_dimensions: dict[str, Any] = {}


@app.route("/")
def index() -> str:
    """Serve a lightweight Three.js-compatible data view."""
    return """
<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>HARIBO Hologram</title></head>
<body><h1>HARIBO OROM – Hologramme</h1><pre id="data">{}</pre>
<script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
<script>
const socket = io();
socket.emit('demande_scan');
socket.on('mise_a_jour', data => {
  document.getElementById('data').textContent = JSON.stringify(data, null, 2);
});
</script></body></html>
"""


@socketio.on("demande_scan")
def handle_scan() -> None:
    flask_socketio.emit("mise_a_jour", donnees_dimensions)


def lancer_serveur(detector_instance: Any, port: int = 5000) -> None:
    """Run the dashboard and periodically broadcast detector data."""

    def boucle_maj() -> None:
        while True:
            global donnees_dimensions
            donnees_dimensions = detector_instance.scan_dimensions()
            socketio.emit("mise_a_jour", donnees_dimensions)
            time.sleep(1)

    threading.Thread(target=boucle_maj, daemon=True).start()
    socketio.run(app, host="0.0.0.0", port=port, allow_unsafe_werkzeug=True)
