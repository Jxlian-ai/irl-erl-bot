# IRL-ERL Trading Bot (One-Click EXE via GitHub Actions)

Upload this repository to GitHub, and the included workflow will automatically build a **Windows .exe** using PyInstaller. 
After the workflow finishes, download the EXE from the "Artifacts" section of the workflow run.

## Quick Steps
1) Create a new GitHub repo (Public or Private).
2) Upload/Drag&Drop all files from this folder into the repo.
3) Go to the repo → **Actions** tab → enable workflows if asked.
4) Wait for the run named **Build EXE (Windows)** to finish.
5) Click the run → **Artifacts** → download `IRL_ERL_Bot_EXE`.
6) Inside the ZIP: run `IRL_ERL_Bot.exe`.

## Local run (optional)
```
pip install -r requirements.txt
streamlit run app.py
```

## Notes
- MetaTrader5 integration is provided as a placeholder (`mt5_bridge.py`). 
  It's disabled by default in `app.py` so the build won't fail on systems without MT5. 
  Later, you can enable it under Settings in the UI.
- The bot stores trades in `trades.db` (SQLite) for journaling.

