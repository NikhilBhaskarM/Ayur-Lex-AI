from urllib.parse import urlparse
import ipaddress
import socket

ALLOWED_DOMAINS = [
    # Official Indian Public Databases
    "indiacode.nic.in",
    "ipindia.gov.in",
    "nbaindia.org",
    "tkdl.res.in",
    "ayush.gov.in",
    "fssai.gov.in",
    "cdsco.gov.in",
    "pcimh.gov.in",
    "gov.in",
    "nic.in",
    "res.in",
    # International Treaties & Databases
    "wipo.int",
    "cbd.int",
    "wto.org",
    "ema.europa.eu",
]

def is_private_ip(url: str) -> bool:
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return False
            
        ip = socket.gethostbyname(hostname)
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except Exception:
        return True # Default to true on error for safety

def is_url_allowed(url: str) -> bool:
    try:
        if is_private_ip(url):
            return False
            
        parsed = urlparse(url)
        hostname = (parsed.hostname or "").lower()
        if not hostname:
            return False
            
        return any(hostname.endswith("." + domain) or hostname == domain for domain in ALLOWED_DOMAINS)
    except Exception:
        return False
