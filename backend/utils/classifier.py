import re

# simple classifier for IP/domain/hash detection

_re_ipv4 = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")
_re_domain = re.compile(r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$")
_re_md5 = re.compile(r"^[a-fA-F0-9]{32}$")
_re_sha1 = re.compile(r"^[a-fA-F0-9]{40}$")
_re_sha256 = re.compile(r"^[a-fA-F0-9]{64}$")

def classify_ioc(value: str) -> str:
    v = value.strip()
    if _re_ipv4.match(v):
        # basic sanity (not full validation of octets)
        return "ip"
    if _re_md5.match(v):
        return "md5"
    if _re_sha1.match(v):
        return "sha1"
    if _re_sha256.match(v):
        return "sha256"
    if _re_domain.match(v):
        return "domain"
    return "unknown"
