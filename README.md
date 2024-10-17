# PyRAT

## A small Trojan written in python for educational purposes

### cfg.py

```
SMTP_SRV='<your_smtp_server>'
SMTP_PORT=<your_smtp_port>
EMAIL='<your_email>'
EMAIL_PASS=<your_email_password>'
```

### Build:

```
pyinstaller --noconsole --onefile main.py
```