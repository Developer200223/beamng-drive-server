#!/usr/bin/env python3

import json
import logging
import os
import zipfile
from pathlib import Path

from flask import Flask, jsonify, render_template_string

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
MOD_DIR = BASE_DIR / "mods"
CONFIG_PATH = BASE_DIR / "config.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "server.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("beamng_server")


def default_config():
    return {
        "host": "0.0.0.0",
        "port": 8080,
        "server_name": "BeamNG Drive Codespaces Server",
        "max_players": 32,
        "mods_enabled": True,
        "mod_directory": "./mods",
    }


def load_config():
    if not CONFIG_PATH.exists():
        config = default_config()
        CONFIG_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")
        logger.info("Created default config.json")
        return config

    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as fh:
            config = json.load(fh)
        for key, value in default_config().items():
            config.setdefault(key, value)
        return config
    except Exception as exc:
        logger.warning("Failed to load config.json: %s; using defaults", exc)
        return default_config()


CONFIG = load_config()
LOG_DIR.mkdir(parents=True, exist_ok=True)
MOD_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)


def load_mods_from_zip(mod_dir: Path):
    mods = []
    for zip_path in sorted(mod_dir.glob("*.zip")):
        try:
            target_dir = mod_dir / zip_path.stem
            target_dir.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(zip_path, "r") as archive:
                archive.extractall(target_dir)
            mods.append(
                {
                    "name": zip_path.name,
                    "directory": zip_path.stem,
                    "size": zip_path.stat().st_size,
                }
            )
            logger.info("Loaded mod: %s", zip_path.name)
        except Exception as exc:
            logger.error("Failed to load mod %s: %s", zip_path.name, exc)
    return mods


@app.route("/")
def index():
    mods = load_mods_from_zip(MOD_DIR) if CONFIG.get("mods_enabled", True) else []
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>{{ server_name }}</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #111827;
                color: #f9fafb;
                margin: 0;
                padding: 32px;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
                background: #1f2937;
                border-radius: 12px;
                padding: 24px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.25);
            }
            h1 { color: #60a5fa; }
            .status-box {
                background: #0f172a;
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 18px;
                margin-bottom: 18px;
            }
            ul { padding-left: 20px; }
            li { margin-bottom: 6px; }
            .meta { color: #cbd5e1; }
            a { color: #93c5fd; text-decoration: none; margin-right: 15px; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚗 {{ server_name }}</h1>
            <div class="status-box">
                <p class="meta">Status: <strong style="color: #4ade80;">● ONLINE</strong></p>
                <p class="meta">Host: {{ host }}</p>
                <p class="meta">Port: {{ port }}</p>
                <p class="meta">Players: {{ players }}/{{ max_players }}</p>
            </div>
            <h2>Loaded Mods ({{ mods|length }})</h2>
            {% if mods %}
                <ul>
                    {% for mod in mods %}
                        <li>{{ mod.name }} ({{ mod.directory }})</li>
                    {% endfor %}
                </ul>
            {% else %}
                <p>No mods loaded yet. Add ZIP files to the <code>mods/</code> folder.</p>
            {% endif %}
            <p>
                <a href="/api/status">📊 API Status</a>
                <a href="/api/mods">📦 Mod List</a>
            </p>
        </div>
    </body>
    </html>
    """
    return render_template_string(
        html,
        server_name=CONFIG.get("server_name", "BeamNG Drive Codespaces Server"),
        host=CONFIG.get("host", "0.0.0.0"),
        port=CONFIG.get("port", 8080),
        players=0,
        max_players=CONFIG.get("max_players", 32),
        mods=mods,
    )


@app.route("/api/status")
def api_status():
    mods = load_mods_from_zip(MOD_DIR) if CONFIG.get("mods_enabled", True) else []
    return jsonify(
        {
            "status": "online",
            "server_name": CONFIG.get("server_name", "BeamNG Drive Codespaces Server"),
            "host": CONFIG.get("host", "0.0.0.0"),
            "port": CONFIG.get("port", 8080),
            "players": 0,
            "max_players": CONFIG.get("max_players", 32),
            "mods": mods,
        }
    )


@app.route("/api/mods")
def api_mods():
    mods = load_mods_from_zip(MOD_DIR) if CONFIG.get("mods_enabled", True) else []
    return jsonify({"mods": mods})


@app.route("/api/reload-mods", methods=["POST"])
def reload_mods():
    try:
        mods = load_mods_from_zip(MOD_DIR) if CONFIG.get("mods_enabled", True) else []
        return jsonify({"success": True, "mods": mods})
    except Exception as exc:
        logger.exception("Failed to reload mods")
        return jsonify({"success": False, "error": str(exc)}), 500


if __name__ == "__main__":
    host = os.getenv("HOST", CONFIG.get("host", "0.0.0.0"))
    port = int(os.getenv("PORT", CONFIG.get("port", 8080)))
    logger.info("Starting BeamNG Drive Codespaces server on %s:%s", host, port)
    app.run(host=host, port=port, debug=False)
