"""
Upload complete VeriVox App repository directly to GitHub using GitHub API (Zero Git required).
"""
import os
import sys
import json
import base64
import urllib.request
import urllib.error

REPO_OWNER = "ta15spec"
REPO_NAME = "verivox_app"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("=" * 70)
print("  VeriVox App Direct GitHub Uploader (Zero Git Required)")
print("=" * 70)
print(f"Target Repository: https://github.com/{REPO_OWNER}/{REPO_NAME}")
print("\nTo upload all files (including .github and app folder):")
print("1. Open: https://github.com/settings/tokens/new")
print("2. Note: 'VeriVox APK Build'")
print("3. Check the box: 'repo' (Full control of private repositories)")
print("4. Scroll to bottom and click 'Generate token'")
print("5. Paste your token below:\n")

try:
    token = input("Enter GitHub Personal Access Token: ").strip()
except Exception:
    token = ""

if not token:
    print("\nError: Token is required to upload files to GitHub. Aborting.")
    input("Press Enter to exit...")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "User-Agent": "VeriVox-Uploader"
}

def get_existing_sha(file_path_in_repo):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path_in_repo}"
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get("sha")
    except urllib.error.HTTPError:
        return None

def upload_file(local_path, repo_path):
    with open(local_path, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode('utf-8')

    sha = get_existing_sha(repo_path)
    payload = {
        "message": f"Upload {repo_path}",
        "content": content_b64,
        "branch": "main"
    }
    if sha:
        payload["sha"] = sha

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{repo_path}"
    data_bytes = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method="PUT")
    try:
        with urllib.request.urlopen(req) as resp:
            return True, None
    except urllib.error.HTTPError as e:
        return False, e.read().decode('utf-8')

print("\nScanning and uploading all files to GitHub...")

count = 0
for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.endswith(('.pyc', '.DS_Store', 'push_to_github.py', 'push_to_github.bat')):
            continue
        local_path = os.path.join(root, f)
        rel_path = os.path.relpath(local_path, BASE_DIR).replace("\\", "/")
        print(f"Uploading: {rel_path} ...", end="", flush=True)
        ok, err = upload_file(local_path, rel_path)
        if ok:
            print(" [OK]")
            count += 1
        else:
            print(f" [ERROR: {err}]")

print("\n" + "=" * 70)
print(f"Uploaded {count} files to https://github.com/{REPO_OWNER}/{REPO_NAME}")
print("Check your Actions tab on GitHub to download the built APK in ~2 minutes:")
print(f"https://github.com/{REPO_OWNER}/{REPO_NAME}/actions")
print("=" * 70 + "\n")
input("Press Enter to exit...")
