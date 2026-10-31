#!/usr/bin/env python3
"""Fetch the latest N V2Ray share links from a public Telegram channel's web preview.

Usage: python feed/scrape.py [channel] [count] [out_file]
Defaults: persianvpnhub 50 feed/configs.txt
Writes one link per line, newest first. Exits non-zero (and leaves the old file) if nothing found.
"""
import html
import re
import sys
import urllib.request

CHANNEL = sys.argv[1] if len(sys.argv) > 1 else "persianvpnhub"
COUNT = int(sys.argv[2]) if len(sys.argv) > 2 else 50
OUT = sys.argv[3] if len(sys.argv) > 3 else "feed/configs.txt"
MAX_PAGES = 8

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")
LINK_RE = re.compile(
    r"(?:vmess|vless|trojan|ss|ssr|socks|hysteria2|hy2|tuic|wireguard)://[^\s<>\"'`]+",
    re.I)
POST_RE = re.compile(
    r'data-post="[^/"]+/(\d+)".*?<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>',
    re.S)
TAG_RE = re.compile(r"<[^>]+>")


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", "replace")


def dedupe_key(link: str) -> str:
    # protocol + userinfo + host:port, ignoring query params and the #name fragment
    base = link.split("#", 1)[0].split("?", 1)[0]
    return base.lower()


def posts(page_html: str):
    """Yield (post_id, [links]) for each post, in page order (oldest -> newest)."""
    for m in POST_RE.finditer(page_html):
        pid = int(m.group(1))
        text = html.unescape(TAG_RE.sub(" ", m.group(2)))
        yield pid, LINK_RE.findall(text)


def main() -> int:
    found, seen = [], set()
    before = None
    for _ in range(MAX_PAGES):
        url = f"https://t.me/s/{CHANNEL}" + (f"?before={before}" if before else "")
        page = fetch(url)
        items = list(posts(page))
        if not items:
            break
        for _pid, links in reversed(items):  # newest first
            for link in links:
                key = dedupe_key(link)
                if key not in seen:
                    seen.add(key)
                    found.append(link)
        if len(found) >= COUNT:
            break
        before = min(pid for pid, _ in items)
    found = found[:COUNT]
    if not found:
        print("no configs found", file=sys.stderr)
        return 1
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(found) + "\n")
    print(f"wrote {len(found)} configs to {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
