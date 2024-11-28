# PyRAT

## A small Trojan written in python for educational purposes

---

### Build
```commandline
python -m nuitka --standalone --onefile --windows-console-mode=disable --windows-icon-from-ico=<icon.ico> --output-filename=<filename.exe> .\victim_startup.py
```