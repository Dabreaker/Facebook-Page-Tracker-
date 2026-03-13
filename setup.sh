#!/bin/bash
echo "[*] Updating packages..."
pkg update && pkg upgrade -y
echo "[*] Installing dependencies..."
pkg install python chromium tur-repo -y
pkg install chromedriver -y
pip install -r requirements.txt
echo "[+] Environment setup complete."

