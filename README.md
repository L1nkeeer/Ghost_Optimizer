# Ghost Optimizer

Ghost Optimizer is an open-source, advanced Windows optimization tool written in Python. It features a modern, cyberpunk-themed Text User Interface (TUI) powered by `rich`, and employs Clean Architecture principles for safe, modular, and extensible system tweaking.

## Features

- **Modern Cyberpunk Dashboard:** Real-time system monitoring (CPU, GPU, RAM, OS info, Admin status) using `rich.layout` and `rich.panel`.
- **Deep Temp Cleaning:** Safely flushes `%TEMP%`, `C:\Windows\Temp`, and `Prefetch`.
- **Network Optimization:** Flushes DNS, resets Winsock, and optimizes TCP auto-tuning.
- **SysMain (Superfetch) Management:** Easily disable SysMain to reduce disk usage.
- **Telemetry Disabler:** Safely disables Windows Telemetry (DiagTrack) via Services and Registry.
- **Clean Architecture:** Modular structure (`core`, `ui`, `tweaks`, `utils`) making it easy to add new tweaks.

## Installation

```bash
git clone https://github.com/L1nkeeer/Ghost_Optimizer.git
cd Ghost_Optimizer
pip install -r requirements.txt
python main.py
```

## Disclaimer

Use this script at your own risk. The author is not responsible for any damage or data loss. It is recommended to create a System Restore Point before applying system tweaks.
