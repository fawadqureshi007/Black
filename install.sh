#!/bin/bash

echo "==================================="
echo "   BlackTrace Auto Installer"
echo "==================================="

echo "[+] Updating system..."
sudo apt update

echo "[+] Creating virtual environment..."
python -m venv blacktrace_env

echo "[+] Activating environment..."
source blacktrace_env/bin/activate

echo "[+] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[+] Installing spaCy model..."
python -m spacy download en_core_web_sm

echo "==================================="
echo " Installation Complete!"
echo " Run: python blacktrace.py"
echo "==================================="
