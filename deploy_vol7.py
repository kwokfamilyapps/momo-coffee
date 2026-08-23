#!/usr/bin/env python3
"""Deploy momo-coffee Vol.7: upload index.html + vol1..vol7.html to GitHub Pages via Contents API."""
import json, urllib.request, base64, time, sys

TOKEN_PATH = "C:/Users/verno/Documents/momo-html/tmp_github_token_b64.txt"
BASE_DIR = "C:/Users/verno/Documents/momo-html/momo-coffee/"
OWNER = "kwokfamilyapps"
REPO = "momo-coffee"

with open(TOKEN_PATH) as f:
    token = base64.b64decode(f.read().strip()).decode()

H = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json",
     "User-Agent": "momo-deploy"}

def api(url, method="GET", data=None):
    req = urllib.request.Request(url, method=method, headers=H)
    if data is not None:
        req.add_header("Content-Type", "application/json")
        req.data = json.dumps(data).encode()
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

def upload(local_name, remote_path):
    with open(BASE_DIR + local_name, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    data = {"message": f"Update {remote_path} (Vol.7)", "content": content, "branch": "main"}
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{remote_path}"
    try:
        data["sha"] = api(url)["sha"]
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
    api(url, method="PUT", data=data)
    print(f"OK upload {remote_path}")

files = ["index.html", "vol1.html", "vol2.html", "vol3.html", "vol4.html", "vol5.html", "vol6.html", "vol7.html"]
for f in files:
    upload(f, f)

print("ALL_UPLOADED")
time.sleep(30)

test_urls = [
    ("root",  f"https://{OWNER}.github.io/{REPO}/",        "Vol.7"),
    ("vol1",  f"https://{OWNER}.github.io/{REPO}/vol1.html", "Vol.1"),
    ("vol2",  f"https://{OWNER}.github.io/{REPO}/vol2.html", "Vol.2"),
    ("vol3",  f"https://{OWNER}.github.io/{REPO}/vol3.html", "Vol.3"),
    ("vol4",  f"https://{OWNER}.github.io/{REPO}/vol4.html", "Vol.4"),
    ("vol5",  f"https://{OWNER}.github.io/{REPO}/vol5.html", "Vol.5"),
    ("vol6",  f"https://{OWNER}.github.io/{REPO}/vol6.html", "Vol.6"),
    ("vol7",  f"https://{OWNER}.github.io/{REPO}/vol7.html", "Vol.7"),
]
fails = 0
for name, url, label in test_urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read().decode("utf-8", errors="replace")
            ok = r.status == 200 and "手沖" in body and label in body
            print(f"{'PASS' if ok else 'FAIL'} {name}: HTTP {r.status} contains-手沖={'手沖' in body} contains-{label}={label in body}")
            if not ok:
                fails += 1
    except Exception as e:
        print(f"FAIL {name}: {e}")
        fails += 1

print(f"VERIFY_DONE fails={fails}")
sys.exit(1 if fails else 0)
