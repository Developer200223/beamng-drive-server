# BeamNG Drive Codespaces Server

This repository is a Codespaces-ready BeamNG Drive server starter with a working local web server and mod loading support.

What it includes:
- Python server with a web status page
- JSON API for server and mod status
- automatic mod loading from the `mods/` folder
- Codespaces/devcontainer configuration
- setup script for first-time startup

Important note:
- This project provides a working server scaffold for hosting in Codespaces and managing mods.
- It does not include the official BeamNG dedicated server binary or proprietary server assets from BeamNG itself.
- To run a real BeamNG multiplayer setup, you still need the official game/server package, compatible files, and any required permissions from BeamNG.

Quick start:
1. Open this repo in GitHub Codespaces.
2. The devcontainer will run `setup.sh` automatically.
3. Start the app:

```bash
python3 server.py
```

4. Open the forwarded port `8080` in Codespaces.

Server endpoints:
- `/` — status page
- `/api/status` — JSON server status
- `/api/mods` — JSON list of loaded mods
- `/api/reload-mods` — POST to reload mods from the `mods/` directory

Mod installation:
- Add `.zip` mod files to the `mods/` folder.
- The app loads them automatically when launched.
- You can also trigger a reload by hitting `/api/reload-mods`.

Configuration:
- Edit `config.json` to change the host, port, and server name.

Project layout:
```text
beamng-drive-server/
├── .devcontainer/
│   └── devcontainer.json
├── mods/
│   └── README.md
├── config.json
├── requirements.txt
├── server.py
├── setup.sh
├── start.sh
├── README.md
└── .gitignore
```
