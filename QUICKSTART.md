# Quick Start Guide

## 1️⃣ Open in Codespaces

Click here to open in Codespaces:
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Developer200223/beamng-drive-server)

## 2️⃣ Run Setup (Automatic)

Codespaces will automatically run `setup.sh` after creation.

If not, run manually:
```bash
bash setup.sh
```

## 3️⃣ Start the Server

```bash
python3 server.py
```

You'll see:
```
🚗 Starting BeamNG Universal Server
============================================================
Server: My BeamNG Universal Server
Listening on 0.0.0.0:8080
📍 Codespaces URL: https://your-codespace-8080.app.github.dev
============================================================
```

## 4️⃣ Access Your Server

- **Browser:** Click the link in the terminal or open:
  - `https://your-codespace-8080.app.github.dev`
  - `http://localhost:8080` (if running locally)

## 5️⃣ Add Mods (Optional)

1. Go to the `mods/` folder
2. Upload or add your `.zip` mod files
3. Restart the server - mods load automatically

## 📊 Check Status

Visit these endpoints:

- **Status Page:** `https://your-codespace:8080/`
- **Server Status API:** `https://your-codespace:8080/api/status`
- **Mods API:** `https://your-codespace:8080/api/mods`

## ⚙️ Configuration

Edit `config.json` to customize:

```json
{
  "server_name": "My Custom Server",
  "max_players": 32,
  "port": 8080,
  "mods_enabled": true
}
```

Then restart the server.

## 🛑 Stop the Server

Press `CTRL+C` in the terminal.

---

**That's it!** Your BeamNG server is now running on Codespaces! 🚗
