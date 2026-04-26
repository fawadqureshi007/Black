#!/usr/bin/env python3

import time
import sys
import os
import re
import json
import webbrowser
import socket
import concurrent.futures
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse, quote
import requests
from collections import Counter

# --- Dependency checks and imports ---
try:
    import requests
except ImportError:
    print("\033[91m[ERROR] 'requests' not found. Run: pip install requests\033[0m")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("\033[91m[ERROR] 'beautifulsoup4' not found. Run: pip install beautifulsoup4\033[0m")
    sys.exit(1)

try:
    from waybackpy import WaybackMachineCDXServerAPI
except ImportError:
    print("\033[91m[ERROR] 'waybackpy' not found. Run: pip install waybackpy\033[0m")
    sys.exit(1)

try:
    import spacy
    SPACY_NLP = spacy.load("en_core_web_sm")
    SPACY_ENABLED = True
except Exception:
    SPACY_ENABLED = False
    print("\033[93m[WARN] 'spacy' or 'en_core_web_sm' missing. Limited entity extraction.\033[0m")

try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, number_type
    PHONENUMBERS_ENABLED = True
except ImportError:
    PHONENUMBERS_ENABLED = False
    print("\033[93m[WARN] 'phonenumbers' missing. Phone analysis disabled.\033[0m")

try:
    import whois
    WHOIS_ENABLED = True
except ImportError:
    WHOIS_ENABLED = False
    print("\033[93m[WARN] 'python-whois' missing. WHOIS lookup disabled.\033[0m")

try:
    import dns.resolver
    DNS_ENABLED = True
except ImportError:
    DNS_ENABLED = False
    print("\033[93m[WARN] 'dnspython' missing. DNS lookup disabled.\033[0m")

try:
    import exifread
    EXIFREAD_ENABLED = True
except ImportError:
    EXIFREAD_ENABLED = False
    print("\033[93m[WARN] 'exifread' missing. EXIF extraction disabled.\033[0m")

# --- Neon color variables ---
NEON_CYAN         = "\033[96m"
NEON_GREEN        = "\033[92m"
NEON_MAGENTA      = "\033[95m"
NEON_YELLOW       = "\033[93m"
NEON_RED          = "\033[91m"
NEON_BLUE         = "\033[94m"
NEON_RESET        = "\033[0m"

NEON_BOLD_CYAN    = "\033[1;96m"
NEON_BOLD_RED     = "\033[1;91m"
NEON_BOLD_GREEN   = "\033[1;92m"
NEON_BOLD_MAGENTA = "\033[1;95m"
NEON_BOLD_YELLOW  = "\033[1;93m"
NEON_BOLD_BLUE    = "\033[1;94m"

# API Keys (You should set these as environment variables for security)
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
HIBP_API_KEY = os.environ.get('HIBP_API_KEY', '')
ABUSEIPDB_KEY = os.environ.get('ABUSEIPDB_KEY', '')

# --- Helper functions ---
                                                            
def print_heading(text, desc=""):
    print(f"\n{NEON_BOLD_GREEN}┌─[ {text} ]{NEON_RESET}")
    if desc:
        print(f"{NEON_GREEN}{desc}{NEON_RESET}\n")

def print_logo():
    logo = NEON_BOLD_CYAN + r"""
██████╗ ██╗      █████╗  ██████╗██╗  ██╗████████╗██████╗  █████╗  ██████╗███████╗
██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝
██████╔╝██║     ███████║██║     █████╔╝    ██║   ██████╔╝███████║██║     █████╗  
██╔══██╗██║     ██╔══██║██║     ██╔═██╗    ██║   ██╔══██╗██╔══██║██║     ██╔══╝  
██████╔╝███████╗██║  ██║╚██████╗██║  ██╗   ██║   ██║  ██║██║  ██║╚██████╗███████╗
╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝

                    Made by Fawad Qureshi
                    Instagram: h4cker_fawad
""" + NEON_RESET
    print(logo)
    print(f"{NEON_BOLD_GREEN}=== DARKNET OSINT RECON PROBE v4.0 ==={NEON_RESET}\n")
    print(f"{NEON_BOLD_YELLOW}Creator: H4CKER_FAWAD | Think like an attacker..{NEON_RESET}\n")

def print_menu():
    print(f"{NEON_BOLD_CYAN}:: SECTION ONE - SCAN OPS & RECON ::{NEON_RESET}\n")
    print(f"{NEON_GREEN} 1  IMAGE GEOLOCATION (EXIF & Tactical Analysis)")
    print(f" 2  SOCIAL MEDIA DEEP DIVE")
    print(f" 3  EMAIL BREACH & SOURCE SWEEP")
    print(f" 4  EMAIL VERIFICATION & INTEL")
    print(f" 5  DOMAIN INTELLIGENCE")
    print(f" 6  METADATA EXTRACTION (Files & EXIF)")
    print(f" 7  GOOGLE DORKING (Ultimate Search Arsenal)")
    print(f" 8  INSTAGRAM RECON (Profile Investigation)")
    print(f" 9  PORT SCAN (Network Reconnaissance)")
    
    print(f"\n{NEON_BOLD_CYAN}:: SECTION TWO - ADVANCED INTEL ::{NEON_RESET}\n")
    print(f"{NEON_GREEN}10  GITHUB RECON (User Intelligence)")
    print(f"11  WEBSITE METADATA & ENTITY SCRAPER")
    print(f"12  PHONE NUMBER HACK-RECON")
    print(f"13  REVERSE IMAGE MISSIONS")
    print(f"14  GEOINT OPS (Satellite & Map Assault)")
    print(f"15  WAYBACK MACHINE DOMINATION")
    print(f"16  IP GEOBLACKLIST RECON")
    print(f"17  THREAT INTEL FEEDS")
    print(f"18  REDDIT RECON (Subreddit & User Analysis)")
    
    print(f"\n{NEON_BOLD_CYAN}:: SYSTEM ::{NEON_RESET}\n")
    print(f"{NEON_GREEN}19  REPORT BUG (Feedback & Issues)")
    print(f"20  EXIT THE MATRIX{NEON_RESET}\n")

def input_menu_choice():
    return input(f"{NEON_BOLD_GREEN}>> Enter your choice [1-20]: {NEON_RESET}").strip()

def create_session():
    """Create a requests session with proper headers"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    return session

# --- Module 1: Image Geolocation ---
def image_geolocation():
    if not EXIFREAD_ENABLED:
        print(f"{NEON_BOLD_RED}[ERROR] 'exifread' missing. Run: pip install exifread{NEON_RESET}")
        return
    print_heading(
        "IMAGE GEOLOCATION",
        "Extract GPS data from image metadata or provide tactical manual guidance."
    )
    img_path = input(f"{NEON_GREEN}Enter path to the target image: {NEON_RESET}").strip()
    if not os.path.exists(img_path):
        print(f"{NEON_BOLD_RED}[ERROR] File not found: {img_path}{NEON_RESET}")
        return
    try:
        with open(img_path, 'rb') as f:
            tags = exifread.process_file(f)
            if not tags:
                print(f"{NEON_YELLOW}[WARN] No EXIF metadata detected. Try Reverse Image module.{NEON_RESET}")
                return
            gps_lat_ref = tags.get('GPS GPSLatitudeRef')
            gps_lat = tags.get('GPS GPSLatitude')
            gps_long_ref = tags.get('GPS GPSLongitudeRef')
            gps_long = tags.get('GPS GPSLongitude')

            if gps_lat and gps_lat_ref and gps_long and gps_long_ref:
                def deg_to_dec(value):
                    d = float(value.values[0].num) / float(value.values[0].den)
                    m = float(value.values[1].num) / float(value.values[1].den)
                    s = float(value.values[2].num) / float(value.values[2].den)
                    return d + (m/60.0) + (s/3600.0)
                lat = deg_to_dec(gps_lat)
                if gps_lat_ref.values[0].upper() == 'S':
                    lat *= -1
                lon = deg_to_dec(gps_long)
                if gps_long_ref.values[0].upper() == 'W':
                    lon *= -1
                print(f"{NEON_BOLD_GREEN}>> Coordinates extracted:{NEON_RESET}")
                print(f"{NEON_CYAN}   Latitude: {lat}")
                print(f"   Longitude: {lon}{NEON_RESET}")
                print(f"\n{NEON_YELLOW}>>> Locate on Google Maps: {NEON_BLUE}https://www.google.com/maps/search/?api=1&query={lat},{lon}{NEON_RESET}")
            else:
                print(f"{NEON_YELLOW}[WARN] No GPS EXIF data present. Manual image analysis recommended.{NEON_RESET}")
    except Exception as e:
        print(f"{NEON_BOLD_RED}[ERROR] Problem processing image: {e}{NEON_RESET}")

# --- Module 2: Social Media Deep Dive ---
def social_media_investigation():
    print_heading(
        "SOCIAL MEDIA DEEP DIVE",
        "Initiate username recon across prime social platforms. Extract profiles like a shadow."
    )
    username = input(f"{NEON_GREEN}Enter target username: {NEON_RESET}").strip()
    if not username:
        print(f"{NEON_BOLD_RED}[ERROR] No username provided.{NEON_RESET}")
        return
    platforms = {
        "FACEBOOK"      : f"https://facebook.com/{username}",
        "TWITTER (X)"   : f"https://twitter.com/{username}",
        "INSTAGRAM"     : f"https://instagram.com/{username}",
        "TELEGRAM"      : f"https://t.me/{username}",
        "LINKEDIN"      : f"https://linkedin.com/in/{username}",
        "GITHUB"        : f"https://github.com/{username}",
        "REDDIT"        : f"https://reddit.com/user/{username}",
        "YOUTUBE"       : f"https://www.youtube.com/{username}",
        "TIKTOK"        : f"https://www.tiktok.com/@{username}",
        "MEDIUM"        : f"https://medium.com/@{username}",
        "PINTEREST"     : f"https://www.pinterest.com/{username}",
        "SNAPCHAT"      : f"https://www.snapchat.com/add/{username}",
        "VIMEO"         : f"https://vimeo.com/{username}",
        "SOUNDCLOUD"    : f"https://soundcloud.com/{username}",
        "TUMBLR"        : f"https://{username}.tumblr.com",
        "QUORA"         : f"https://www.quora.com/profile/{username}",
        "STEAM"         : f"https://steamcommunity.com/id/{username}",
        "TWITCH"        : f"https://twitch.tv/{username}",
        "PATREON"       : f"https://www.patreon.com/{username}",
        "BLOGGER"       : f"https://{username}.blogspot.com",
        "GOODREADS"     : f"https://www.goodreads.com/{username}",
        "VK"            : f"https://vk.com/{username}",
        "OK.RU"         : f"https://ok.ru/{username}",
        "DRIBBBLE"      : f"https://dribbble.com/{username}",
        "FLICKR"        : f"https://www.flickr.com/people/{username}",
        "HACKERNEWS"    : f"https://news.ycombinator.com/user?id={username}",
        "BADOO"         : f"https://badoo.com/profile/{username}",
        "ELLO"          : f"https://ello.co/{username}",
        "DEVIANTART"    : f"https://www.deviantart.com/{username}",
        "MIXCLOUD"      : f"https://www.mixcloud.com/{username}/",
        "PERISCOPE"     : f"https://www.pscp.tv/{username}",
    }
    print(f"\n{NEON_BOLD_GREEN}[*] Profiles found for {NEON_BOLD_MAGENTA}{username}{NEON_BOLD_GREEN}:{NEON_RESET}")
    for plat, url in platforms.items():
        print(f"{NEON_CYAN}{plat.ljust(15)}{NEON_YELLOW} --> {NEON_BLUE}{url}{NEON_RESET}")
    print(f"\n{NEON_YELLOW}Harness external tools like WhatsMyName for further deep recon.{NEON_RESET}")

# --- Module 3: Email Breach & Source Sweep ---
def email_analysis():
    print_heading(
        "EMAIL BREACH & SOURCE SWEEP",
        "Probe email breach databases and scrape public paste content."
    )
    email = input(f"{NEON_GREEN}Target email: {NEON_RESET}").strip()
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        print(f"{NEON_BOLD_RED}[ERROR] Email format invalid.{NEON_RESET}")
        return
    hibp_api_key = HIBP_API_KEY
    if hibp_api_key == "":
        print(f"{NEON_YELLOW}[!] HIBP API key unset. Skipping breach automation.{NEON_RESET}")
        print(f"Manual Check: https://haveibeenpwned.com/Account/PwnedWebsites")
    else:
        try:
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            headers = {"hibp-api-key": hibp_api_key, "user-agent": "DARKNET-OSINT-3.0"}
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                breaches = r.json()
                print(f"{NEON_BOLD_GREEN}[+] {len(breaches)} breaches detected for {email}:{NEON_RESET}")
                for entry in breaches:
                    print(f"  - {NEON_RED}{entry['Name']}{NEON_RESET} on {entry['BreachDate']}")
            elif r.status_code == 404:
                print(f"{NEON_BOLD_GREEN}[+] No breaches found for target.{NEON_RESET}")
            else:
                print(f"{NEON_BOLD_RED}[ERROR] HIBP HTTP {r.status_code}{NEON_RESET}")
        except Exception as e:
            print(f"{NEON_BOLD_RED}[ERROR] HIBP request failed: {e}{NEON_RESET}")

    print(f"\n{NEON_CYAN}--- Scanning Pastebin Public Pastes ---{NEON_RESET}")
    try:
        pastebin_url = "https://scrape.pastebin.com/api_scraping.php?limit=50"
        r = requests.get(pastebin_url, timeout=10)
        if r.status_code == 200:
            pastes = r.json()
            hits = []
            print(f"{NEON_YELLOW}[i] Checking recent pastes for presence of email...{NEON_RESET}")
            for p in pastes:
                key = p.get('key')
                if key:
                    try:
                        content = requests.get(f"https://pastebin.com/raw/{key}", timeout=5).text
                        if email.lower() in content.lower():
                            hits.append(f"https://pastebin.com/{key}")
                    except:
                        pass
                time.sleep(0.5)
            if hits:
                print(f"{NEON_BOLD_GREEN}[+] Found {len(hits)} pastes containing target email:{NEON_RESET}")
                for link in hits:
                    print(f"  > {NEON_BLUE}{link}{NEON_RESET}")
            else:
                print(f"{NEON_YELLOW}[-] No recent pastes found relating to target.{NEON_RESET}")
    except:
        print(f"{NEON_BOLD_RED}[ERROR] Pastebin scrape failed.{NEON_RESET}")

    print(f"\n{NEON_MAGENTA}Launching deep Google search for traces...{NEON_RESET}")
    webbrowser.open(f"https://www.google.com/search?q=\"{email}\"")

# --- Module 4: Email Verification & Intel ---
def email_lookup_and_verification():
    print_heading(
        "EMAIL VERIFICATION & INTEL",
        "Via Hunter.io & manual reverse lookup portals."
    )
    email = input(f"{NEON_GREEN}Enter email for verification: {NEON_RESET}").strip()
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        print(f"{NEON_BOLD_RED}[ERROR] Invalid email format.{NEON_RESET}")
        return
    hunter_api_key = "YOUR_HUNTER_IO_API_KEY"
    if hunter_api_key == "YOUR_HUNTER_IO_API_KEY":
        print(f"{NEON_YELLOW}[!] Hunter.io API key missing. Skipping automated verification.{NEON_RESET}")
        print(f"Manual: https://hunter.io/verify")
    else:
        print(f"\n{NEON_CYAN}--- Hunter.io API Query ---{NEON_RESET}")
        try:
            r = requests.get(f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={hunter_api_key}", timeout=10)
            if r.status_code == 200:
                data = r.json().get('data', {})
                print(f"Status   : {data.get('status', 'Unknown')}")
                print(f"Result   : {data.get('result', 'Unknown')}")
                print(f"Score    : {data.get('score', 'N/A')}")
                disp = f"{NEON_BOLD_RED}Yes{NEON_RESET}" if data.get('disposable') else "No"
                print(f"Disposable: {disp}")
                mx = f"{NEON_BOLD_RED}Missing{NEON_RESET}" if not data.get('mx_records') else "Present"
                print(f"MX Records: {mx}")
                print(f"SMTP Check: {data.get('smtp_check')}")
                sources = data.get('sources', [])
                if sources:
                    print(f"Source Domains (Top 3):")
                    for s in sources[:3]:
                        print(f"  - {NEON_BLUE}{s.get('domain')} {NEON_YELLOW}({s.get('uri')}){NEON_RESET}")
            else:
                print(f"{NEON_BOLD_RED}[ERROR] Hunter.io HTTP {r.status_code}{NEON_RESET}")
        except Exception as e:
            print(f"{NEON_BOLD_RED}[ERROR] Hunter.io request failed: {e}{NEON_RESET}")

    print(f"\n{NEON_YELLOW}Manual Lookup Portals:{NEON_RESET}")
    print(f"- ReverseContact: {NEON_BLUE}https://www.reversecontact.com/{NEON_RESET}")
    print(f"- Epieos       : {NEON_BLUE}https://epieos.com/{NEON_RESET}\n")

# --- Module 5: Domain Intelligence ---
def find_subdomains_crtsh(domain, max_attempts=3, delay=7):
    print(f"\n{NEON_CYAN}[*] Harvesting subdomains from crt.sh...{NEON_RESET}")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    headers = {'User-Agent': 'DARKNET-OSINT-SUITE'}
    subs = set()
    for attempt in range(max_attempts):
        try:
            r = requests.get(url, headers=headers, timeout=40)
            if r.status_code == 200:
                data = r.json()
                for entry in data:
                    name_val = entry.get('name_value','')
                    for sub in name_val.split('\n'):
                        sub = sub.strip().strip('.')
                        if sub.endswith('.' + domain) or sub == domain:
                            subs.add(sub)
                break
            else:
                print(f"{NEON_YELLOW}[WARN] crt.sh HTTP {r.status_code}, try {attempt+1}/{max_attempts}{NEON_RESET}")
        except Exception as ex:
            print(f"{NEON_YELLOW}[WARN] crt.sh attempt {attempt+1} error: {ex}{NEON_RESET}")
        if attempt < max_attempts-1:
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)
    if subs:
        print(f"{NEON_BOLD_GREEN}[+] Subdomain haul: {len(subs)} found:{NEON_RESET}")
        for s in sorted(subs):
            print(f" - {NEON_BLUE}{s}{NEON_RESET}")
    else:
        print(f"{NEON_YELLOW}[-] No subdomains or failed after retries.{NEON_RESET}")
    return sorted(subs)

def domain_investigation():
    if not WHOIS_ENABLED or not DNS_ENABLED:
        print(f"{NEON_BOLD_RED}[ERROR] Required modules missing. Install python-whois and dnspython{NEON_RESET}")
        return

    print_heading(
        "DOMAIN INTELLIGENCE",
        "WHOIS records, DNS, and subdomain reconnaissance."
    )
    target = input(f"{NEON_GREEN}Give domain or URL: {NEON_RESET}").strip()
    if not target:
        print(f"{NEON_BOLD_RED}[ERROR] No target provided.{NEON_RESET}")
        return

    if target.startswith(('http://','https://')):
        target = target.split("://")[1].split('/')[0]

    try:
        import tldextract
        ext = tldextract.extract(target)
        if not ext.domain or not ext.suffix:
            print(f"{NEON_BOLD_RED}[ERROR] Invalid domain source.{NEON_RESET}")
            return
        domain = f"{ext.domain}.{ext.suffix}"
    except ImportError:
        domain = target
        print(f"{NEON_YELLOW}[WARN] tldextract not available, using raw input{NEON_RESET}")
    
    print(f"{NEON_CYAN}Analyzing domain: {NEON_BOLD_GREEN}{domain}{NEON_RESET}")

    print(f"\n{NEON_MAGENTA}--- WHOIS Information ---{NEON_RESET}\n")
    try:
        w_info = whois.whois(domain)
        registrar = ", ".join(w_info.registrar) if isinstance(w_info.registrar, list) else w_info.registrar or "N/A"
        print(f"Registrar    : {registrar}\n")

        c_date = w_info.creation_date[0] if isinstance(w_info.creation_date, list) else w_info.creation_date
        c_str = c_date.strftime('%Y-%m-%d %H:%M:%S') if isinstance(c_date, datetime) else "UNK"
        print(f"Created      : {c_str}\n")

        if isinstance(c_date, datetime):
            days_alive = (datetime.now() - c_date).days
            print(f"Domain Age   : {days_alive} days\n")

        e_date = w_info.expiration_date[0] if isinstance(w_info.expiration_date, list) else w_info.expiration_date
        e_str = e_date.strftime('%Y-%m-%d %H:%M:%S') if isinstance(e_date, datetime) else "UNK"
        print(f"Expires      : {e_str}\n")

        ns = ", ".join(w_info.name_servers) if w_info.name_servers else "None"
        print(f"Name Servers : {ns}\n")

        status = w_info.status
        if status:
            status_str = ", ".join(status) if isinstance(status, list) else status
            print(f"Status       : {status_str}\n")

    except Exception as e:
        print(f"{NEON_BOLD_RED}[ERROR] WHOIS failed: {e}{NEON_RESET}")

    print(f"\n{NEON_MAGENTA}--- DNS Records (A / MX / NS) ---{NEON_RESET}\n")
    try:
        for rtype in ['A','MX','NS']:
            answers = dns.resolver.resolve(domain, rtype)
            print(f"{rtype} Records:")
            for rdata in answers:
                if rtype == 'NS':
                    print(f" - {rdata.target.to_text()}")
                else:
                    print(f" - {rdata.to_text()}")
            print()
    except Exception:
        pass

    find_subdomains_crtsh(domain)

# --- Module 6: Metadata Extraction ---
def metadata_extraction():
    if not EXIFREAD_ENABLED:
        print(f"{NEON_BOLD_RED}[ERROR] exifread missing. Run: pip install exifread{NEON_RESET}")
        return
    print_heading(
        "METADATA EXTRACTION",
        "Decrypt EXIF and file data. Unveil hidden digital footprints."
    )
    file_path = input(f"{NEON_GREEN}Target file path: {NEON_RESET}").strip()
    if not os.path.exists(file_path):
        print(f"{NEON_BOLD_RED}[ERROR] File does not exist.{NEON_RESET}")
        return
    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f, details=False)
            if not tags:
                print(f"{NEON_YELLOW}[WARN] No EXIF metadata found.{NEON_RESET}")
                stats = os.stat(file_path)
                print(f"Size    : {stats.st_size} bytes")
                print(f"Created : {datetime.fromtimestamp(stats.st_ctime)}")
                print(f"Modified: {datetime.fromtimestamp(stats.st_mtime)}")
                print(f"{NEON_YELLOW}For full forensic analysis, use ExifTool: https://exiftool.org/{NEON_RESET}")
                return
            print(f"{NEON_BOLD_GREEN}EXIF Metadata:{NEON_RESET}")
            for t in sorted(tags):
                if t not in ('JPEGThumbnail','TIFFThumbnail','Filename','EXIF MakerNote'):
                    print(f"{NEON_CYAN}{t.ljust(40)}: {NEON_YELLOW}{tags[t]}{NEON_RESET}")
    except Exception as e:
        print(f"{NEON_BOLD_RED}[ERROR] Cannot process file: {e}{NEON_RESET}")

# --- Module 7: Google Dorking ---
def google_dorking():
    print_heading(
        "GOOGLE DORKING",
        "Inject advanced search payloads. Reveal secrets hidden in plain sight."
    )
    examples = [
        'site:secretcorp.com confidential',
        'filetype:pdf "internal use only"',
        'intitle:"index of" passwords',
        'inurl:admin inurl:login',
        'intext:"internal use only"'
    ]
    print(f"Sample Dorks:")
    for x in examples:
        print(f"  {NEON_CYAN}{x}{NEON_RESET}")
    dork = input(f"{NEON_GREEN}Your dork query: {NEON_RESET}").strip()
    if not dork:
        print(f"{NEON_BOLD_RED}[ERROR] No query provided.{NEON_RESET}")
        return
    print(f"{NEON_YELLOW}Deploying search...{NEON_RESET}")
    webbrowser.open(f"https://www.google.com/search?q={dork}")

# --- Module 8: Instagram Recon ---
def instagram_recon():
    print_heading(
        "INSTAGRAM RECON",
        "Investigate Instagram profiles and extract available information."
    )
    username = input(f"{NEON_GREEN}Enter Instagram username: {NEON_RESET}").strip()
    
    if not username:
        print(f"{NEON_BOLD_RED}[ERROR] Username cannot be empty!{NEON_RESET}")
        return
    
    url = f"https://www.instagram.com/{username}/"
    
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to find profile information
            title = soup.find('title')
            if title:
                print(f"{NEON_BLUE}Profile Title:{NEON_RESET} {NEON_YELLOW}{title.text}{NEON_RESET}")
            
            # Look for meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                print(f"{NEON_BLUE}Description:{NEON_RESET} {NEON_YELLOW}{meta_desc.get('content', 'N/A')}{NEON_RESET}")
            
            # Extract Twitter and YouTube from description if available
            desc_content = meta_desc.get('content', '') if meta_desc else ''
            twitter_match = re.search(r'Twitter: (@?\w+)', desc_content)
            youtube_match = re.search(r'YouTube: (https?://[^\s]+)', desc_content)
            
            if twitter_match:
                print(f"{NEON_BLUE}Twitter:{NEON_RESET} {NEON_YELLOW}{twitter_match.group(1)}{NEON_RESET}")
            
            if youtube_match:
                print(f"{NEON_BLUE}YouTube:{NEON_RESET} {NEON_YELLOW}{youtube_match.group(1)}{NEON_RESET}")
            
            print(f"{NEON_BLUE}Profile URL:{NEON_RESET} {NEON_YELLOW}{url}{NEON_RESET}")
            print(f"{NEON_BLUE}Status:{NEON_RESET} {NEON_YELLOW}Profile exists{NEON_RESET}")
            
        elif response.status_code == 404:
            print(f"{NEON_RED}Profile not found{NEON_RESET}")
        else:
            print(f"{NEON_RED}Error: HTTP {response.status_code}{NEON_RESET}")
            
    except requests.RequestException as e:
        print(f"{NEON_RED}Error accessing Instagram: {e}{NEON_RESET}")

# --- Module 9: Port Scan ---
def port_scan():
    print_heading(
        "PORT SCAN",
        "Network reconnaissance through port scanning of target systems."
    )
    target = input(f"{NEON_GREEN}Enter target IP or domain: {NEON_RESET}").strip()
    
    if not target:
        print(f"{NEON_BOLD_RED}[ERROR] Target cannot be empty!{NEON_RESET}")
        return
    
    try:
        # Resolve domain to IP if needed
        try:
            target_ip = socket.gethostbyname(target)
        except socket.gaierror:
            print(f"{NEON_RED}Could not resolve domain{NEON_RESET}")
            return
        
        print(f"\n{NEON_BOLD_GREEN}Scanning {target} ({target_ip})...{NEON_RESET}")
        
        # Common ports to scan
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
        
        open_ports = []
        
        def check_port(port):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex((target_ip, port))
                    if result == 0:
                        try:
                            service = socket.getservbyport(port, 'tcp')
                        except:
                            service = 'Unknown'
                        open_ports.append((port, service))
                        print(f"{NEON_GREEN}[+] Port {port} ({service}) is open{NEON_RESET}")
                    else:
                        print(f"{NEON_RED}[-] Port {port} is closed{NEON_RESET}")
            except (socket.timeout, socket.error):
                print(f"{NEON_RED}[-] Port {port} filtered or host unreachable{NEON_RESET}")
            except Exception as e:
                print(f"{NEON_RED}[-] Error scanning port {port}: {e}{NEON_RESET}")
        
        # Use threading to speed up the scan
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(check_port, common_ports)
        
        if open_ports:
            print(f"\n{NEON_BOLD_GREEN}Open ports found:{NEON_RESET}")
            for port, service in open_ports:
                print(f"{NEON_GREEN}Port {port} ({service}){NEON_RESET}")
        else:
            print(f"\n{NEON_RED}No open ports found{NEON_RESET}")
            
    except Exception as e:
        print(f"{NEON_RED}Error during port scan: {e}{NEON_RESET}")

# --- Module 10: GitHub Recon ---
def github_recon():
    print_heading(
        "GITHUB RECON",
        "Gather intelligence on GitHub users and their activities."
    )
    username = input(f"{NEON_GREEN}Enter GitHub username: {NEON_RESET}").strip()
    
    if not username:
        print(f"{NEON_BOLD_RED}[ERROR] Username cannot be empty!{NEON_RESET}")
        return
    
    url = f"https://api.github.com/users/{username}"
    headers = {}
    
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            
            print(f"\n{NEON_BOLD_GREEN}GitHub User Information:{NEON_RESET}")
            print(f"{NEON_GREEN}Username: {user_data.get('login', 'N/A')}{NEON_RESET}")
            print(f"{NEON_YELLOW}Name: {user_data.get('name', 'N/A')}{NEON_RESET}")
            print(f"{NEON_GREEN}Bio: {user_data.get('bio', 'N/A')}{NEON_RESET}")
            print(f"{NEON_YELLOW}Public Repos: {user_data.get('public_repos', 'N/A')}{NEON_RESET}")
            print(f"{NEON_GREEN}Public Gists: {user_data.get('public_gists', 'N/A')}{NEON_RESET}")
            print(f"{NEON_YELLOW}Followers: {user_data.get('followers', 'N/A')}{NEON_RESET}")
            print(f"{NEON_GREEN}Following: {user_data.get('following', 'N/A')}{NEON_RESET}")
            print(f"{NEON_YELLOW}Created At: {user_data.get('created_at', 'N/A')}{NEON_RESET}")
            print(f"{NEON_GREEN}Updated At: {user_data.get('updated_at', 'N/A')}{NEON_RESET}")
            print(f"{NEON_YELLOW}URL: {user_data.get('html_url', 'N/A')}{NEON_RESET}")
            print(f"{NEON_GREEN}Blog: {user_data.get('blog', 'N/A')}{NEON_RESET}")
            print(f"{NEON_YELLOW}Location: {user_data.get('location', 'N/A')}{NEON_RESET}")
            print(f"{NEON_GREEN}Company: {user_data.get('company', 'N/A')}{NEON_RESET}")
            print(f"{NEON_YELLOW}Twitter: {user_data.get('twitter_username', 'N/A')}{NEON_RESET}")
            
        elif response.status_code == 404:
            print(f"{NEON_RED}User not found{NEON_RESET}")
        else:
            print(f"{NEON_RED}Error: HTTP {response.status_code}{NEON_RESET}")
            
    except requests.RequestException as e:
        print(f"{NEON_RED}Error retrieving GitHub information: {e}{NEON_RESET}")

# --- Module 11: Website Metadata & Entity Scraper ---
def website_metadata_and_entity_scraper():
    print_heading(
        "WEBSITE METADATA & ENTITY SCRAPER",
        "Deep crawl URLs in 'urls.txt', extract titles, meta, emails, persons, locations."
    )
    if not SPACY_ENABLED:
        print(f"{NEON_YELLOW}[ WARN ] Spacy model not loaded. Entity extraction disabled.{NEON_RESET}")
    try:
        with open("urls.txt") as f:
            urls = [u.strip() for u in f if u.strip()]
    except:
        print(f"{NEON_BOLD_RED}[ERROR] Cannot open 'urls.txt'. Create it in this folder with one URL per line.{NEON_RESET}")
        return

    headers = {"User-Agent":"DARKNET-OSINT-SUITE/3.0"}
    
    def extract_emails(text):
        return sorted(set(re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text, re.I)))

    def extract_entities(text, labels):
        if not SPACY_ENABLED:
            return []
        doc = SPACY_NLP(text)
        return sorted(set(ent.text for ent in doc.ents if ent.label_ in labels))

    results = {}

    for url in urls:
        print(f"\n{NEON_MAGENTA}[SCRAPING] {url}{NEON_RESET}")
        try:
            r = requests.get(url, headers=headers, timeout=15)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, 'html.parser')

            title = soup.title.string.strip() if soup.title else "N/A"
            meta_tags = {}
            for m in soup.find_all("meta"):
                if 'content' in m.attrs and ('name' in m.attrs or 'property' in m.attrs):
                    key = m.attrs.get("name") or m.attrs.get("property")
                    meta_tags[key.lower()] = m.attrs["content"]

            emails = extract_emails(r.text)
            visible_text = soup.get_text(separator=" ", strip=True)
            names = extract_entities(visible_text, ["PERSON"])
            locations = extract_entities(visible_text, ["GPE", "LOC"])

            results[url] = dict(title=title, meta_tags=meta_tags, emails=emails, names=names, locations=locations)

            print(f"Title        : {NEON_CYAN}{title}{NEON_RESET}")
            print(f"Meta Tags    : {NEON_YELLOW}{len(meta_tags)} found{NEON_RESET}")
            print(f"Emails       : {NEON_YELLOW}{len(emails)} found{NEON_RESET}")
            print(f"Persons      : {NEON_YELLOW}{len(names)} found{NEON_RESET}")
            print(f"Locations    : {NEON_YELLOW}{len(locations)} found{NEON_RESET}")
        except Exception as ex:
            print(f"{NEON_BOLD_RED}[FAILED] {ex}{NEON_RESET}")
            results[url] = {"error": str(ex)}

    try:
        with open("metadata_output.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(f"\n{NEON_BOLD_GREEN}[DONE] Saved scraping data to metadata_output.json{NEON_RESET}")
    except Exception as e:
        print(f"{NEON_BOLD_RED}[ERROR] Saving data failed: {e}{NEON_RESET}")

# --- Module 12: Phone Number Hack-Recon ---
def phone_number_lookup():
    if not PHONENUMBERS_ENABLED:
        print(f"{NEON_BOLD_RED}[ERROR] phonenumbers module missing. Run: pip install phonenumbers{NEON_RESET}")
        return
    print_heading(
        "PHONE NUMBER HACK-RECON",
        "Validate and extract telecom info; generate attack dorks."
    )
    print(f"Example number: {NEON_BOLD_CYAN}+14085551234{NEON_RESET}")
    number = input(f"{NEON_GREEN}Enter full phone number: {NEON_RESET}").strip()
    if not number:
        print(f"{NEON_BOLD_RED}[ERROR] No input given.{NEON_RESET}")
        return
    try:
        parsed = phonenumbers.parse(number, None)
        valid = phonenumbers.is_valid_number(parsed)
        possible = phonenumbers.is_possible_number(parsed)
        if not possible:
            print(f"{NEON_BOLD_RED}[ERROR] Number is not possible.{NEON_RESET}")
            return
        print(f"Valid Number  : {NEON_GREEN if valid else NEON_RED}{valid}{NEON_RESET}")
        print(f"Intl Format   : {NEON_CYAN}{phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}{NEON_RESET}")
        print(f"Nat Format    : {NEON_CYAN}{phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)}{NEON_RESET}")
        print(f"Geo Location  : {NEON_YELLOW}{geocoder.description_for_number(parsed, 'en')}{NEON_RESET}")
        print(f"Carrier      : {NEON_YELLOW}{carrier.name_for_number(parsed, 'en')}{NEON_RESET}")
        num_type = number_type(parsed)
        type_map = {
            0: "Unknown", 1: "Fixed Line", 2: "Mobile", 3: "Fixed Line or Mobile",
            4: "Toll Free", 5: "Premium Rate", 6: "Shared Cost", 7: "VoIP",
            8: "Personal Number", 9: "Pager", 10: "UAN"
        }
        print(f"Type         : {NEON_CYAN}{type_map.get(num_type, 'Unknown')}{NEON_RESET}")

        print(f"\n{NEON_MAGENTA}--- Suggested Google Dorks ---{NEON_RESET}")
        e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        nat = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
        e164_clean = re.sub(r'\D', '', e164)
        nat_clean = re.sub(r'\D', '', nat)
        print(f'  "{NEON_YELLOW}{e164}{NEON_RESET}" OR "{NEON_YELLOW}{nat}{NEON_RESET}"')
        print(f'  "{NEON_YELLOW}{e164_clean}{NEON_RESET}" OR "{NEON_YELLOW}{nat_clean}{NEON_RESET}"')

    except Exception as e:
        print(f"{NEON_BOLD_RED}[ERROR] Parsing failure: {e}{NEON_RESET}")

# --- Module 13: Reverse Image Missions ---
def reverse_image_search():
    print_heading(
        "REVERSE IMAGE MISSIONS",
        "Deploy visual reconnaissance on popular reverse image engines."
    )
    engines = {
        "Google Images"  : "https://images.google.com/",
        "TinEye"         : "https://tineye.com/",
        "Yandex"         : "https://yandex.com/images/",
        "Bing Visual"    : "https://www.bing.com/images/discover",
        "Baidu"          : "https://image.baidu.com/",
        "SauceNAO"       : "https://saucenao.com/",
        "ImgOps"         : "https://imgops.com/"
    }
    for name, url in engines.items():
        print(f"{NEON_CYAN}{name.ljust(18)} {NEON_YELLOW}>>{NEON_RESET} {NEON_BLUE}{url}{NEON_RESET}")
    input(f"\n{NEON_MAGENTA}Hit ENTER to return...{NEON_RESET}")

# --- Module 14: Geospatial Intelligence Operations ---
def geospatial_intelligence():
    print_heading(
        "GEOSPATIAL INTELLIGENCE OPERATIONS",
        "Visualize coordinates or places with satellite layers."
    )
    inp = input(f"{NEON_GREEN}Enter coords (lat,lon) or location name: {NEON_RESET}").strip()
    if not inp:
        print(f"{NEON_BOLD_RED}[ERROR] No input received. Exiting to menu.{NEON_RESET}")
        return

    lat, lon = None, None
    coords_valid = False
    try:
        parts = [p.strip() for p in inp.split(',')]
        if len(parts) == 2:
            lat = float(parts[0])
            lon = float(parts[1])
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                coords_valid = True
    except:
        coords_valid = False

    if coords_valid:
        print(f"{NEON_BOLD_GREEN}[+] Valid coordinate input: {lat}, {lon}{NEON_RESET}")
        google_sat = f"https://www.google.com/maps/@{lat},{lon},15z/data=!5m1!1e4"
        osm_map = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=15/{lat}/{lon}"
    else:
        print(f"{NEON_YELLOW}[-] Coordinates invalid or absent; treating input as place query.{NEON_RESET}")
        query = inp.replace(' ', '+')
        google_sat = f"https://www.google.com/maps/search/?api=1&query={query}&layer=c"
        osm_map = f"https://www.openstreetmap.org/search?query={query}"

    print(f"{NEON_CYAN}Opening Google Satellite Map...{NEON_RESET}")
    webbrowser.open(google_sat)
    print(f"{NEON_CYAN}Opening OpenStreetMap view...{NEON_RESET}")
    webbrowser.open(osm_map)
    print(f"\n{NEON_BOLD_GREEN}[DONE] Geospatial ops loaded in default browser.{NEON_RESET}")

# --- Module 15: Wayback Machine Domination ---
def wayback_machine_lookup():
    print_heading(
        "WAYBACK MACHINE DOMINATION",
        "Raid web archives. Reconstruct the digital past."
    )
    url = input(f"{NEON_GREEN}Enter URL (include http/https): {NEON_RESET}").strip()
    if not url.startswith(('http://','https://')):
        print(f"{NEON_BOLD_RED}[ERROR] URL must start with http:// or https://{NEON_RESET}")
        return
    user_agent = "DARKNET-OSINT-SUITE/3.0"
    try:
        api = WaybackMachineCDXServerAPI(url, user_agent)
        snaps = list(api.snapshots())
        if not snaps:
            print(f"{NEON_YELLOW}[-] No archived snapshots found.{NEON_RESET}")
            return
        print(f"{NEON_BOLD_GREEN}[+] {len(snaps)} archives located. Listing top 10:{NEON_RESET}")
        for i, snap in enumerate(snaps[:10]):
            try:
                ts = datetime.strptime(snap.timestamp, "%Y%m%d%H%M%S")
                ts_formatted = ts.strftime("%Y-%m-%d %H:%M:%S")
            except:
                ts_formatted = snap.timestamp
            print(f" [{NEON_CYAN}{i+1}{NEON_RESET}] {NEON_BLUE}{snap.archive_url}{NEON_RESET} (Captured: {ts_formatted}, HTTP {snap.statuscode})")
    except Exception as e:
        print(f"{NEON_BOLD_RED}[ERROR] Wayback Machine API issue: {e}{NEON_RESET}")

# --- Module 16: IP Geoblacklist Recon ---
def ip_geolocation_blacklist():
    print_heading(
        "IP GEOBLACKLIST RECON",
        "Trace location, abuse reports, and expose hostile IP infrastructure."
    )
    ip = input(f"{NEON_GREEN}Target IP: {NEON_RESET}").strip()
    if not ip:
        print(f"{NEON_BOLD_RED}[ERROR] No IP entered.{NEON_RESET}")
        return
    try:
        import ipaddress
        ipaddress.ip_address(ip)
    except:
        print(f"{NEON_BOLD_RED}[ERROR] Invalid IP address syntax.{NEON_RESET}")
        return
    
    try:
        geo_resp = requests.get(f"https://ipinfo.io/{ip}/json")
        if geo_resp.status_code != 200:
            print(f"{NEON_BOLD_RED}[ERROR] ipinfo.io geo lookup failed.{NEON_RESET}")
            return
        geo = geo_resp.json()
        for k in ("ip","hostname","city","region","country","loc","org","postal","timezone"):
            print(f"{NEON_CYAN}{k.capitalize().ljust(10)}:{NEON_YELLOW} {geo.get(k,'N/A')}{NEON_RESET}")
    except Exception as e:
        print(f"{NEON_BOLD_RED}[ERROR] Geo lookup failure: {e}{NEON_RESET}")
        return

    print(f"\n{NEON_MAGENTA}--- AbuseIPDB Report ---{NEON_RESET}\n")
    abuseipdb_key = "ABUSEIPDB_KEY"
    if abuseipdb_key == "":
        print(f"{NEON_YELLOW}[!] AbuseIPDB key missing. Skipping abuse report.{NEON_RESET}")
        return
    try:
        headers = {'Accept':'application/json','Key':abuseipdb_key}
        resp = requests.get(f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays=90", headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json().get('data',{})
            score = data.get('abuseConfidenceScore',0)
            reports = data.get('totalReports',0)
            status_msg = f"Potentially Malicious IP" if score>0 else "No significant abuse reports"
            color = NEON_BOLD_RED if score>0 else NEON_BOLD_GREEN
            print(f"Abuse Confidence Score : {color}{score}%{NEON_RESET}")
            print(f"Total Reports (90d)    : {color}{reports}{NEON_RESET}")
            print(f"Status                 : {color}{status_msg}{NEON_RESET}\n")
            if score > 0:
                for rep in data.get('reports', [])[:3]:
                    print(f"  - [{NEON_CYAN}{rep.get('reportedAt','N/A')}{NEON_RESET}] {rep.get('comment','No comment')}")
                if len(data.get('reports', [])) > 3:
                    print(f"  ... and {len(data['reports'])-3} more")
        else:
            print(f"{NEON_BOLD_RED}[ERROR] AbuseIPDB HTTP {resp.status_code}{NEON_RESET}")
    except Exception as e:
        print(f"{NEON_BOLD_RED}[ERROR] AbuseIPDB API call failed: {e}{NEON_RESET}")

# --- Module 17: Threat Intel Feeds ---
def threat_intel_feeds():
    print_heading(
        "THREAT INTEL FEEDS",
        "Access real-time threat intelligence from various sources."
    )
    
    print(f"{NEON_BOLD_GREEN}Available Threat Intelligence Sources:{NEON_RESET}")
    
    feeds = {
        "AlienVault OTX": "https://otx.alienvault.com/",
        "CISA Known Exploited Vulnerabilities": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
        "ThreatFox IOC Database": "https://threatfox.abuse.ch/",
        "MalwareBazaar": "https://bazaar.abuse.ch/",
        "URLhaus": "https://urlhaus.abuse.ch/",
        "Emerging Threats Rules": "https://rules.emergingthreats.net/",
        "FireEye Threat Intelligence": "https://www.fireeye.com/blog/threat-research.html",
        "CrowdStrike Intel": "https://www.crowdstrike.com/blog/",
        "Kaspersky Threat Intelligence": "https://www.kaspersky.com/blog/",
    }
    
    for name, url in feeds.items():
        print(f"{NEON_CYAN}{name.ljust(45)}: {NEON_YELLOW}{url}{NEON_RESET}")
        
    choice = input(f"\n{NEON_GREEN}Open all in browser? (y/N): {NEON_RESET}").strip().lower()
    
    if choice == 'y':
        for url in feeds.values():
            webbrowser.open(url)
            time.sleep(1)

# --- Module 18: Reddit Recon ---
def reddit_recon():
    print_heading(
        "REDDIT RECON (SUBREDDIT & USER ANALYSIS)",
        "Comprehensive Reddit intelligence with data scraping and export capabilities."
    )
    
    print(f"{NEON_CYAN}1. User Analysis")
    print(f"2. Subreddit Analysis")
    print(f"3. Search Posts/Comments{NEON_RESET}")
    
    analysis_type = input(f"{NEON_GREEN}Select analysis type (1-3): {NEON_RESET}").strip()
    
    if analysis_type == "1":
        reddit_user_analysis()
    elif analysis_type == "2":
        reddit_subreddit_analysis()
    elif analysis_type == "3":
        reddit_search_analysis()
    else:
        print(f"{NEON_RED}Invalid selection{NEON_RESET}")

def reddit_user_analysis():
    """Comprehensive Reddit user analysis with data scraping"""
    username = input(f"{NEON_GREEN}Enter Reddit username: {NEON_RESET}").strip()
    if not username:
        print(f"{NEON_RED}No username provided{NEON_RESET}")
        return
    
    username = username.replace('u/', '').replace('/u/', '')
    
    print(f"\n{NEON_YELLOW}[*] Analyzing user: u/{username}{NEON_RESET}")
    
    session = create_session()
    
    user_data = {
        "username": username,
        "analysis_date": datetime.now().isoformat(),
        "profile_info": {},
        "posts": [],
        "comments": [],
        "statistics": {}
    }
    
    # Get user profile info
    print(f"{NEON_CYAN}[*] Fetching profile information...{NEON_RESET}")
    profile_url = f"https://www.reddit.com/user/{username}/about.json"
    
    try:
        response = session.get(profile_url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            user_data["profile_info"] = data.get('data', {})
            
            print(f"{NEON_GREEN}✓ Profile information retrieved{NEON_RESET}")
            print(f"   Name: {user_data['profile_info'].get('name', 'N/A')}")
            print(f"   Karma: {user_data['profile_info'].get('total_karma', 0)}")
            print(f"   Created: {datetime.fromtimestamp(user_data['profile_info'].get('created_utc', 0)).strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"{NEON_RED}✗ Failed to fetch profile: HTTP {response.status_code}{NEON_RESET}")
    except Exception as e:
        print(f"{NEON_RED}✗ Error fetching profile: {e}{NEON_RESET}")
    
    # Get user posts
    print(f"{NEON_CYAN}[*] Fetching user posts...{NEON_RESET}")
    posts_url = f"https://www.reddit.com/user/{username}/submitted.json?limit=100"
    
    try:
        response = session.get(posts_url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            for post in posts:
                post_data = post.get('data', {})
                user_data["posts"].append({
                    "id": post_data.get('id'),
                    "title": post_data.get('title'),
                    "subreddit": post_data.get('subreddit'),
                    "score": post_data.get('score'),
                    "upvote_ratio": post_data.get('upvote_ratio'),
                    "num_comments": post_data.get('num_comments'),
                    "created_utc": post_data.get('created_utc'),
                    "url": post_data.get('url'),
                    "selftext": post_data.get('selftext', '')[:500] + '...' if post_data.get('selftext') else None,
                    "permalink": f"https://reddit.com{post_data.get('permalink')}"
                })
            
            print(f"{NEON_GREEN}✓ Retrieved {len(user_data['posts'])} posts{NEON_RESET}")
        else:
            print(f"{NEON_RED}✗ Failed to fetch posts: HTTP {response.status_code}{NEON_RESET}")
    except Exception as e:
        print(f"{NEON_RED}✗ Error fetching posts: {e}{NEON_RESET}")
    
    # Get user comments
    print(f"{NEON_CYAN}[*] Fetching user comments...{NEON_RESET}")
    comments_url = f"https://www.reddit.com/user/{username}/comments.json?limit=100"
    
    try:
        response = session.get(comments_url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            comments = data.get('data', {}).get('children', [])
            
            for comment in comments:
                comment_data = comment.get('data', {})
                user_data["comments"].append({
                    "id": comment_data.get('id'),
                    "subreddit": comment_data.get('subreddit'),
                    "score": comment_data.get('score'),
                    "created_utc": comment_data.get('created_utc'),
                    "permalink": f"https://reddit.com{comment_data.get('permalink')}",
                    "body": comment_data.get('body', '')[:300] + '...' if comment_data.get('body') else None,
                    "post_title": comment_data.get('link_title')
                })
            
            print(f"{NEON_GREEN}✓ Retrieved {len(user_data['comments'])} comments{NEON_RESET}")
        else:
            print(f"{NEON_RED}✗ Failed to fetch comments: HTTP {response.status_code}{NEON_RESET}")
    except Exception as e:
        print(f"{NEON_RED}✗ Error fetching comments: {e}{NEON_RESET}")
    
    # Calculate statistics
    if user_data["posts"]:
        user_data["statistics"]["total_posts"] = len(user_data["posts"])
        user_data["statistics"]["avg_post_score"] = sum(p["score"] for p in user_data["posts"]) / len(user_data["posts"])
        user_data["statistics"]["most_active_subreddits"] = get_most_common([p["subreddit"] for p in user_data["posts"]])
    
    if user_data["comments"]:
        user_data["statistics"]["total_comments"] = len(user_data["comments"])
        user_data["statistics"]["avg_comment_score"] = sum(c["score"] for c in user_data["comments"]) / len(user_data["comments"])
        user_data["statistics"]["most_commented_subreddits"] = get_most_common([c["subreddit"] for c in user_data["comments"]])
    
    # Save data to files
    save_reddit_data(user_data, f"reddit_user_{username}")
    
    # Display summary
    print(f"\n{NEON_BOLD_GREEN}=== ANALYSIS SUMMARY ==={NEON_RESET}")
    print(f"Username: u/{username}")
    print(f"Total Karma: {user_data['profile_info'].get('total_karma', 'N/A')}")
    print(f"Post Karma: {user_data['profile_info'].get('link_karma', 'N/A')}")
    print(f"Comment Karma: {user_data['profile_info'].get('comment_karma', 'N/A')}")
    print(f"Account Age: {calculate_account_age(user_data['profile_info'].get('created_utc', 0))} days")
    
    if user_data["posts"]:
        print(f"Posts Analyzed: {len(user_data['posts'])}")
        print(f"Avg Post Score: {user_data['statistics']['avg_post_score']:.2f}")
        print(f"Top Subreddits: {', '.join([s[0] for s in user_data['statistics']['most_active_subreddits'][:3]])}")
    
    if user_data["comments"]:
        print(f"Comments Analyzed: {len(user_data['comments'])}")
        print(f"Avg Comment Score: {user_data['statistics']['avg_comment_score']:.2f}")
        print(f"Top Commented: {', '.join([s[0] for s in user_data['statistics']['most_commented_subreddits'][:3]])}")

def reddit_subreddit_analysis():
    """Comprehensive subreddit analysis"""
    subreddit = input(f"{NEON_GREEN}Enter subreddit name: {NEON_RESET}").strip()
    if not subreddit:
        print(f"{NEON_RED}No subreddit provided{NEON_RESET}")
        return
    
    subreddit = subreddit.replace('r/', '').replace('/r/', '')
    
    print(f"\n{NEON_YELLOW}[*] Analyzing subreddit: r/{subreddit}{NEON_RESET}")
    
    session = create_session()
    
    sub_data = {
        "subreddit": subreddit,
        "analysis_date": datetime.now().isoformat(),
        "about_info": {},
        "hot_posts": [],
        "top_posts": [],
        "statistics": {}
    }
    
    # Get subreddit info
    print(f"{NEON_CYAN}[*] Fetching subreddit information...{NEON_RESET}")
    about_url = f"https://www.reddit.com/r/{subreddit}/about.json"
    
    try:
        response = session.get(about_url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            sub_data["about_info"] = data.get('data', {})
            
            print(f"{NEON_GREEN}✓ Subreddit information retrieved{NEON_RESET}")
            print(f"   Name: r/{sub_data['about_info'].get('display_name', 'N/A')}")
            
            # Fix: Check if subscribers is a number before formatting
            subscribers = sub_data['about_info'].get('subscribers')
            if isinstance(subscribers, int):
                print(f"   Subscribers: {subscribers:,}")
            else:
                print(f"   Subscribers: N/A")
                
            print(f"   Created: {datetime.fromtimestamp(sub_data['about_info'].get('created_utc', 0)).strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"{NEON_RED}✗ Failed to fetch subreddit info: HTTP {response.status_code}{NEON_RESET}")
    except Exception as e:
        print(f"{NEON_RED}✗ Error fetching subreddit info: {e}{NEON_RESET}")
    
    # Get hot posts
    print(f"{NEON_CYAN}[*] Fetching hot posts...{NEON_RESET}")
    hot_url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=50"
    
    try:
        response = session.get(hot_url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            for post in posts:
                post_data = post.get('data', {})
                sub_data["hot_posts"].append({
                    "id": post_data.get('id'),
                    "title": post_data.get('title'),
                    "author": post_data.get('author'),
                    "score": post_data.get('score'),
                    "upvote_ratio": post_data.get('upvote_ratio'),
                    "num_comments": post_data.get('num_comments'),
                    "created_utc": post_data.get('created_utc'),
                    "url": post_data.get('url'),
                    "permalink": f"https://reddit.com{post_data.get('permalink')}",
                    "domain": post_data.get('domain'),
                    "is_self": post_data.get('is_self')
                })
            
            print(f"{NEON_GREEN}✓ Retrieved {len(sub_data['hot_posts'])} hot posts{NEON_RESET}")
        else:
            print(f"{NEON_RED}✗ Failed to fetch hot posts: HTTP {response.status_code}{NEON_RESET}")
    except Exception as e:
        print(f"{NEON_RED}✗ Error fetching hot posts: {e}{NEON_RESET}")
    
    # Get top posts
    print(f"{NEON_CYAN}[*] Fetching top posts...{NEON_RESET}")
    top_url = f"https://www.reddit.com/r/{subreddit}/top.json?limit=50&t=month"
    
    try:
        response = session.get(top_url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            for post in posts:
                post_data = post.get('data', {})
                sub_data["top_posts"].append({
                    "id": post_data.get('id'),
                    "title": post_data.get('title'),
                    "author": post_data.get('author'),
                    "score": post_data.get('score'),
                    "upvote_ratio": post_data.get('upvote_ratio'),
                    "num_comments": post_data.get('num_comments'),
                    "created_utc": post_data.get('created_utc'),
                    "url": post_data.get('url'),
                    "permalink": f"https://reddit.com{post_data.get('permalink')}",
                    "domain": post_data.get('domain'),
                    "is_self": post_data.get('is_self')
                })
            
            print(f"{NEON_GREEN}✓ Retrieved {len(sub_data['top_posts'])} top posts{NEON_RESET}")
        else:
            print(f"{NEON_RED}✗ Failed to fetch top posts: HTTP {response.status_code}{NEON_RESET}")
    except Exception as e:
        print(f"{NEON_RED}✗ Error fetching top posts: {e}{NEON_RESET}")
    
    # Calculate statistics
    if sub_data["hot_posts"]:
        sub_data["statistics"]["avg_hot_score"] = sum(p["score"] for p in sub_data["hot_posts"]) / len(sub_data["hot_posts"])
        sub_data["statistics"]["avg_hot_comments"] = sum(p["num_comments"] for p in sub_data["hot_posts"]) / len(sub_data["hot_posts"])
        sub_data["statistics"]["top_hot_authors"] = get_most_common([p["author"] for p in sub_data["hot_posts"] if p["author"] != "[deleted]"])
    
    if sub_data["top_posts"]:
        sub_data["statistics"]["avg_top_score"] = sum(p["score"] for p in sub_data["top_posts"]) / len(sub_data["top_posts"])
        sub_data["statistics"]["avg_top_comments"] = sum(p["num_comments"] for p in sub_data["top_posts"]) / len(sub_data["top_posts"])
        sub_data["statistics"]["top_top_authors"] = get_most_common([p["author"] for p in sub_data["top_posts"] if p["author"] != "[deleted]"])
    
    # Save data to files
    save_reddit_data(sub_data, f"reddit_subreddit_{subreddit}")
    
    # Display summary - fix the formatting here too
    print(f"\n{NEON_BOLD_GREEN}=== SUBREDDIT SUMMARY ==={NEON_RESET}")
    print(f"Subreddit: r/{subreddit}")
    
    # Fix: Check if subscribers is a number before formatting
    subscribers = sub_data['about_info'].get('subscribers')
    if isinstance(subscribers, int):
        print(f"Subscribers: {subscribers:,}")
    else:
        print(f"Subscribers: N/A")
    
    # Fix: Check if active_user_count is a number before formatting
    active_users = sub_data['about_info'].get('active_user_count')
    if isinstance(active_users, int):
        print(f"Active Users: {active_users:,}")
    else:
        print(f"Active Users: N/A")
        
    print(f"Description: {sub_data['about_info'].get('public_description', 'N/A')[:100]}...")
    
    if sub_data["hot_posts"]:
        print(f"Hot Posts Analyzed: {len(sub_data['hot_posts'])}")
        print(f"Avg Hot Score: {sub_data['statistics']['avg_hot_score']:.2f}")
        print(f"Avg Hot Comments: {sub_data['statistics']['avg_hot_comments']:.2f}")
    
    if sub_data["top_posts"]:
        print(f"Top Posts Analyzed: {len(sub_data['top_posts'])}")
        print(f"Avg Top Score: {sub_data['statistics']['avg_top_score']:.2f}")
        print(f"Avg Top Comments: {sub_data['statistics']['avg_top_comments']:.2f}")

def reddit_search_analysis():
    """Search Reddit for specific content"""
    query = input(f"{NEON_GREEN}Enter search query: {NEON_RESET}").strip()
    if not query:
        print(f"{NEON_RED}No query provided{NEON_RESET}")
        return
    
    print(f"\n{NEON_YELLOW}[*] Searching Reddit for: {query}{NEON_RESET}")
    
    session = create_session()
    
    search_data = {
        "query": query,
        "analysis_date": datetime.now().isoformat(),
        "posts": [],
        "comments": [],
        "statistics": {}
    }
    
    # Search posts
    print(f"{NEON_CYAN}[*] Searching posts...{NEON_RESET}")
    search_url = f"https://www.reddit.com/search.json?q={quote(query)}&type=link&limit=100"
    
    try:
        response = session.get(search_url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            for post in posts:
                post_data = post.get('data', {})
                search_data["posts"].append({
                    "id": post_data.get('id'),
                    "title": post_data.get('title'),
                    "author": post_data.get('author'),
                    "subreddit": post_data.get('subreddit'),
                    "score": post_data.get('score'),
                    "num_comments": post_data.get('num_comments'),
                    "created_utc": post_data.get('created_utc'),
                    "url": post_data.get('url'),
                    "permalink": f"https://reddit.com{post_data.get('permalink')}",
                    "selftext": post_data.get('selftext', '')[:300] + '...' if post_data.get('selftext') else None
                })
            
            print(f"{NEON_GREEN}✓ Found {len(search_data['posts'])} posts{NEON_RESET}")
        else:
            print(f"{NEON_RED}✗ Failed to search posts: HTTP {response.status_code}{NEON_RESET}")
    except Exception as e:
        print(f"{NEON_RED}✗ Error searching posts: {e}{NEON_RESET}")
    
    # Search comments
    print(f"{NEON_CYAN}[*] Searching comments...{NEON_RESET}")
    comment_search_url = f"https://www.reddit.com/search.json?q={quote(query)}&type=comment&limit=100"
    
    try:
        response = session.get(comment_search_url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            comments = data.get('data', {}).get('children', [])
            
            for comment in comments:
                comment_data = comment.get('data', {})
                search_data["comments"].append({
                    "id": comment_data.get('id'),
                    "author": comment_data.get('author'),
                    "subreddit": comment_data.get('subreddit'),
                    "score": comment_data.get('score'),
                    "created_utc": comment_data.get('created_utc'),
                    "permalink": f"https://reddit.com{comment_data.get('permalink')}",
                    "body": comment_data.get('body', '')[:200] + '...' if comment_data.get('body') else None,
                    "post_title": comment_data.get('link_title')
                })
            
            print(f"{NEON_GREEN}✓ Found {len(search_data['comments'])} comments{NEON_RESET}")
        else:
            print(f"{NEON_RED}✗ Failed to search comments: HTTP {response.status_code}{NEON_RESET}")
    except Exception as e:
        print(f"{NEON_RED}✗ Error searching comments: {e}{NEON_RESET}")
    
    # Calculate statistics
    if search_data["posts"]:
        search_data["statistics"]["total_posts"] = len(search_data["posts"])
        search_data["statistics"]["avg_post_score"] = sum(p["score"] for p in search_data["posts"]) / len(search_data["posts"])
        search_data["statistics"]["top_subreddits_posts"] = get_most_common([p["subreddit"] for p in search_data["posts"]])
        search_data["statistics"]["top_authors_posts"] = get_most_common([p["author"] for p in search_data["posts"] if p["author"] != "[deleted]"])
    
    if search_data["comments"]:
        search_data["statistics"]["total_comments"] = len(search_data["comments"])
        search_data["statistics"]["avg_comment_score"] = sum(c["score"] for c in search_data["comments"]) / len(search_data["comments"])
        search_data["statistics"]["top_subreddits_comments"] = get_most_common([c["subreddit"] for c in search_data["comments"]])
        search_data["statistics"]["top_authors_comments"] = get_most_common([c["author"] for c in search_data["comments"] if c["author"] != "[deleted]"])
    
    # Save data to files
    save_reddit_data(search_data, f"reddit_search_{query.replace(' ', '_')}")
    
    # Display summary with proper color formatting
    print(f"\n{NEON_BOLD_GREEN}=== SEARCH SUMMARY ==={NEON_RESET}")
    print(f"{NEON_CYAN}Query:{NEON_RESET} {NEON_YELLOW}{query}{NEON_RESET}")
    print(f"{NEON_CYAN}Total Posts Found:{NEON_RESET} {NEON_YELLOW}{len(search_data['posts'])}{NEON_RESET}")
    print(f"{NEON_CYAN}Total Comments Found:{NEON_RESET} {NEON_YELLOW}{len(search_data['comments'])}{NEON_RESET}")
    
    if search_data["posts"]:
        print(f"{NEON_CYAN}Avg Post Score:{NEON_RESET} {NEON_YELLOW}{search_data['statistics']['avg_post_score']:.2f}{NEON_RESET}")
        print(f"{NEON_CYAN}Top Subreddits (Posts):{NEON_RESET} {NEON_YELLOW}{', '.join([s[0] for s in search_data['statistics']['top_subreddits_posts'][:3]])}{NEON_RESET}")
    
    if search_data["comments"]:
        print(f"{NEON_CYAN}Avg Comment Score:{NEON_RESET} {NEON_YELLOW}{search_data['statistics']['avg_comment_score']:.2f}{NEON_RESET}")
        print(f"{NEON_CYAN}Top Subreddits (Comments):{NEON_RESET} {NEON_YELLOW}{', '.join([s[0] for s in search_data['statistics']['top_subreddits_comments'][:3]])}{NEON_RESET}")

# --- Helper functions for Reddit module ---
def get_most_common(items, limit=5):
    """Get most common items from a list"""
    return Counter(items).most_common(limit)

def calculate_account_age(created_utc):
    """Calculate account age in days"""
    if not created_utc:
        return 0
    created_dt = datetime.fromtimestamp(created_utc)
    return (datetime.now() - created_dt).days

def save_reddit_data(data, filename):
    """Save Reddit data to multiple formats"""
    import csv
    
    # Create output directory if it doesn't exist
    os.makedirs("reddit_exports", exist_ok=True)
    base_path = f"reddit_exports/{filename}"
    
    try:
        # Save as JSON (full data)
        with open(f"{base_path}_full.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        # Save summary as JSON
        summary = {
            "metadata": {
                "type": list(data.keys())[1],  # Second key indicates type
                "analysis_date": data.get("analysis_date"),
                "query": data.get("query") or data.get("username") or data.get("subreddit")
            },
            "statistics": data.get("statistics", {})
        }
        
        with open(f"{base_path}_summary.json", 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
        
        # Save posts to CSV if available
        if "posts" in data and data["posts"]:
            with open(f"{base_path}_posts.csv", 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data["posts"][0].keys())
                writer.writeheader()
                writer.writerows(data["posts"])
        
        # Save comments to CSV if available
        if "comments" in data and data["comments"]:
            with open(f"{base_path}_comments.csv", 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data["comments"][0].keys())
                writer.writeheader()
                writer.writerows(data["comments"])
        
        # Save hot posts to CSV if available
        if "hot_posts" in data and data["hot_posts"]:
            with open(f"{base_path}_hot_posts.csv", 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data["hot_posts"][0].keys())
                writer.writeheader()
                writer.writerows(data["hot_posts"])
        
        # Save top posts to CSV if available
        if "top_posts" in data and data["top_posts"]:
            with open(f"{base_path}_top_posts.csv", 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data["top_posts"][0].keys())
                writer.writeheader()
                writer.writerows(data["top_posts"])
        
        print(f"{NEON_GREEN}✓ Data saved to reddit_exports/{filename}_*.{NEON_RESET}")
        
    except Exception as e:
        print(f"{NEON_RED}✗ Error saving data: {e}{NEON_RESET}")

# --- Module 19: Report Bug ---
def report_bug():
    print_heading(
        "REPORT BUG",
        "Provide feedback, report issues, or request new features."
    )
    print(f"{NEON_YELLOW}If you found a bug or have a feature request, please:{NEON_RESET}")
    print(f"{NEON_GREEN}1. Check if the issue has already been reported{NEON_RESET}")
    print(f"{NEON_GREEN}2. Provide detailed information about the bug{NEON_RESET}")
    print(f"{NEON_GREEN}3. Include steps to reproduce the issue{NEON_RESET}")
    print(f"{NEON_GREEN}4. Share your environment details (OS, Python version){NEON_RESET}")
    print(f"\n{NEON_YELLOW}You can report issues at: https://github.com/techenthusiast/Darknet-OSINT/issues{NEON_RESET}")
    print(f"\n{NEON_YELLOW}For security vulnerabilities, please report responsibly.{NEON_RESET}")

# --- Module 20: Exit ---
def exit_program():
    print(f"\n{NEON_BOLD_YELLOW}>> Exiting DARKNET OSINT SUITE. Stay concealed, operator.{NEON_RESET}\n")
    sys.exit(0)

# --- Main Controller ---
def main():
    print_logo()
    while True:
        print_menu()
        choice = input_menu_choice()
        try:
            c = int(choice)
        except ValueError:
            print(f"{NEON_BOLD_RED}[ERROR] Invalid input. Choose 1-20.{NEON_RESET}")
            continue

        # Dispatch module functions
        if c == 1:
            image_geolocation()
        elif c == 2:
            social_media_investigation()
        elif c == 3:
            email_analysis()
        elif c == 4:
            email_lookup_and_verification()
        elif c == 5:
            domain_investigation()
        elif c == 6:
            metadata_extraction()
        elif c == 7:
            google_dorking()
        elif c == 8:
            instagram_recon()
        elif c == 9:
            port_scan()
        elif c == 10:
            github_recon()
        elif c == 11:
            website_metadata_and_entity_scraper()
        elif c == 12:
            phone_number_lookup()
        elif c == 13:
            reverse_image_search()
        elif c == 14:
            geospatial_intelligence()
        elif c == 15:
            wayback_machine_lookup()
        elif c == 16:
            ip_geolocation_blacklist()
        elif c == 17:
            threat_intel_feeds()
        elif c == 18:
            reddit_recon()
        elif c == 19:
            report_bug()
        elif c == 20:
            exit_program()
        else:
            print(f"{NEON_BOLD_RED}[ERROR] Choice must be between 1 and 20.{NEON_RESET}")

        print("\n" + NEON_BOLD_GREEN + "="*70 + NEON_RESET + "\n")

if __name__ == "__main__":
    main()
