#!/bin/bash

echo "==================================="
echo "   BlackTrace Auto Installer"
echo "==================================="

set -e

echo "[+] Updating system..."
sudo apt update -y

echo "[+] Creating virtual environment..."
python3 -m venv blacktrace_env

echo "[+] Upgrading pip..."
./blacktrace_env/bin/pip install --upgrade pip

echo "[+] Installing dependencies..."
./blacktrace_env/bin/pip install -r requirements.txt

echo "[+] Installing spaCy model..."
./blacktrace_env/bin/python -m spacy download en_core_web_sm

echo "==================================="
echo " Installation Complete!"
echo ""
echo "▶ To run BlackTrace:"
echo "   ./run.sh"
echo "   OR"
echo "   ./blacktrace_env/bin/python blacktrace.py"
echo "==================================="
