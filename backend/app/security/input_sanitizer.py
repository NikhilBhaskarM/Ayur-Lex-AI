import re

MALICIOUS_PATTERNS = [
    r"(?i)ignore\s+(all\s+)?previous\s+instructions",
    r"(?i)system\s*(prompt)?:",
    r"(?i)system\s+override",
    r"(?i)<script\b",
    r"(?i)<\?xml",
    r"(?i)you\s+are\s+now\s+(a\s+)?malicious",
    r"(?i)disregard\s+all\s+rules",
]

def is_potentially_malicious(text: str) -> bool:
    for pattern in MALICIOUS_PATTERNS:
        if re.search(pattern, text):
            return True
    return False

def sanitize_user_input(text: str) -> str:
    sanitized = text
    for pattern in MALICIOUS_PATTERNS:
        sanitized = re.sub(pattern, "[REDACTED]", sanitized)
    return sanitized

def sanitize_llm_output(text: str) -> str:
    # Remove potential markdown image exfiltration
    sanitized = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    return sanitized
