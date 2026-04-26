#!/bin/bash

echo "==================================="
echo "   BlackTrace Auto Installer"
echo "==================================="

echo "[+] Updating system..."
sudo apt update -y

echo "[+] Creating virtual environment..."
python3 -m venv blacktrace_env

echo "[+] Activating environment..."
source blacktrace_env/bin/activate

echo "[+] Upgrading pip..."
pip install --upgrade pip

echo "[+] Installing dependencies..."
pip install -r requirements.txt

echo "[+] Installing spaCy model..."
python3 -m spacy download en_core_web_sm

echo "==================================="
echo " Installation Complete!"
echo " Run:"
echo "   source blacktrace_env/bin/activate"
echo "   python3 blacktrace.py"
echo "==================================="
