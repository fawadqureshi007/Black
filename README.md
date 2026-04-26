
````md
# 🕶️ BlackTrace  
### Darknet OSINT Recon Probe

```bash
██████╗ ██╗      █████╗  ██████╗██╗  ██╗████████╗██████╗  █████╗  ██████╗███████╗
██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝
██████╔╝██║     ███████║██║     █████╔╝    ██║   ██████╔╝███████║██║     █████╗  
██╔══██╗██║     ██╔══██║██║     ██╔═██╗    ██║   ██╔══██╗██╔══██║██║     ██╔══╝  
██████╔╝███████╗██║  ██║╚██████╗██║  ██╗   ██║   ██║  ██║██║  ██║╚██████╗███████╗
╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝
````

> ⚡ Stay concealed. Trace everything.

---

## 📌 Overview

BlackTrace is an advanced **Open Source Intelligence (OSINT) toolkit** built in Python for cybersecurity research, digital investigations, and reconnaissance operations.

It provides a unified CLI interface combining multiple intelligence-gathering techniques into one powerful framework.

---

## 🚀 Features

* 📍 Image GPS extraction (EXIF analysis)
* 🌐 Username search across 30+ platforms
* 📧 Email breach detection & paste search
* 🔎 Email verification via OSINT APIs
* 🌍 WHOIS, DNS & subdomain enumeration
* 📂 Metadata extraction from files
* 🧠 Google Dorking automation
* 🕰️ Wayback Machine historical lookup
* 🌐 IP geolocation & abuse check
* 📊 Website scraping with NLP entity extraction
* 📱 Phone number intelligence
* 🖼️ Reverse image search (multi-engine)
* 🛰️ GEOINT (Maps + Satellite analysis)
* 📡 Port scanning & network reconnaissance
* 🧠 Threat intelligence feeds

---

## ⚙️ Prerequisites

* Python 3.7+
* pip package manager
* Internet connection

---

## 🧪 Installation

### 🔧 Quick Install (Recommended)

```bash
git clone https://github.com/fawadqureshi007/Black.git
cd Black
chmod +x install.sh
./install.sh
```

---

### 🛠️ Manual Install

```bash
sudo apt update

python -m venv blacktrace_env
source blacktrace_env/bin/activate

pip install -r requirements.txt

python -m spacy download en_core_web_sm
```

---

## ▶️ Run Tool

```bash
python blacktrace.py
```

> ⚠️ If `python` does not work, use `python3`.

---

## 📦 requirements.txt

```
requests
beautifulsoup4
waybackpy
spacy
phonenumbers
exifread
tldextract
python-whois
dnspython
```

---

## 🧠 Modules

| #  | Module              | Description             |
| -- | ------------------- | ----------------------- |
| 1  | Image GeoLocation   | Extract GPS from images |
| 2  | Social Recon        | Username tracking       |
| 3  | Email Breach Scan   | Leak detection          |
| 4  | Email Verification  | Email validation        |
| 5  | Domain Intelligence | WHOIS + DNS             |
| 6  | Metadata Extraction | Hidden file data        |
| 7  | Google Dorking      | Advanced search         |
| 8  | Instagram Recon     | Profile analysis        |
| 9  | Port Scanner        | Network scanning        |
| 10 | GitHub Recon        | Developer profiling     |
| 11 | Website Scraper     | Metadata extraction     |
| 12 | Phone Intel         | Carrier & geo lookup    |
| 13 | Reverse Image       | Image OSINT             |
| 14 | GEOINT Ops          | Satellite mapping       |
| 15 | Wayback Analysis    | Historical pages        |
| 16 | IP Intelligence     | Abuse reports           |
| 17 | Threat Feeds        | Cyber threat data       |
| 18 | Reddit Recon        | Community intelligence  |
| 19 | Bug Report          | Issue reporting         |
| 20 | Exit                | Safe shutdown           |

---

## 🔑 API Setup

Some modules require API keys:

* HaveIBeenPwned → [https://haveibeenpwned.com/API/Key](https://haveibeenpwned.com/API/Key)
* Hunter.io → [https://hunter.io](https://hunter.io)
* AbuseIPDB → [https://www.abuseipdb.com/api](https://www.abuseipdb.com/api)

### Set keys:

```bash
export HIBP_API_KEY="your_key"
export ABUSEIPDB_KEY="your_key"
export GITHUB_TOKEN="your_token"
```

---

## ⚖️ Ethical Use

✔ Allowed:

* Educational use
* Security research
* Authorized penetration testing

❌ Not allowed:

* Unauthorized tracking
* Privacy invasion
* Illegal activities

---

## 🛡️ Disclaimer

This tool is for **educational and authorized security testing only**.
The developer is not responsible for misuse.

---

## 👤 Author

**Fawad Qureshi--**
📸 Instagram: 
[https://www.instagram.com/h4cker_fawad/](https://www.instagram.com/h4cker_fawad/)


---

## ⭐ Support

If you like this project:

* ⭐ Star the repo
* 🍴 Fork it
* 🚀 Share it with cybersecurity community


