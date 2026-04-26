#!/bin/bash

echo "==================================="
echo "   BlackTrace Auto Installer"
echo "==================================="

set -e

echo "[+] Updating system..."
sudo apt update -y

echo "[+] Creating virtual environment..."
python3 -m venv blacktrace_env

echo "[+] Installing dependencies..."
./blacktrace_env/bin/pip install --upgrade pip
./blacktrace_env/bin/pip install -r requirements.txt

echo "[+] Checking spaCy model..."
./blacktrace_env/bin/python -c "
import spacy
try:
    spacy.load('en_core_web_sm')
    print('[+] spaCy model already installed')
except:
    print('[+] Installing spaCy model...')
    import os
    os.system('./blacktrace_env/bin/python -m spacy download en_core_web_sm')
"

echo "==================================="
echo " Installation Complete!"
echo ""
echo "▶ Run BlackTrace:"
echo "   ./run.sh"
echo "==================================="
