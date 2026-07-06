from __future__ import annotations
import re
def truncate(s: str, n: int) -> str: return s if len(s) <= n else s[: n-1] + "..."
def escape_html(s: str) -> str:
    if not s: return ""
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def mask_token(s: str, n: int = 4) -> str:
    if not s: return ""
    if len(s) <= 2*n: return "*" * len(s)
    return s[:n] + "*"*(len(s)-2*n) + s[-n:]
EMAIL_RE = re.compile(r"[^@]+@[^@]+\\.[^@]+")
def is_email(s: str) -> bool: return bool(s and EMAIL_RE.match(s))
