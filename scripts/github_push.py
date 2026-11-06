"""
AgriVision: Automated GitHub Repository Creation and Push Tool
"""
import os
import sys

# Ensure UTF-8 console output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import json
import subprocess
import urllib.request
import urllib.error

def run_cmd(cmd_list, cwd=None):
    res = subprocess.run(cmd_list, cwd=cwd, capture_output=True, text=True)
    return res.returncode, res.stdout.strip(), res.stderr.strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/github_push.py <GITHUB_PAT>")
        sys.exit(1)

    token = sys.argv[1].strip()
    repo_name = "agrivision"
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    print("==================================================")
    print("[*] AgriVision GitHub Repo Creator & Auto-Pusher")
    print("==================================================")
    print(f"Target repository: {repo_name}")
    print(f"Project directory: {project_root}")

    # 1. Verify GitHub Token
    print("\n[1/4] Verifying GitHub Personal Access Token...")
    req = urllib.request.Request(
        "https://api.github.com/user",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "AgriVision-Setup"
        }
    )
    try:
        with urllib.request.urlopen(req) as response:
            user_data = json.loads(response.read().decode())
            github_username = user_data.get("login")
            print(f"[+] Authenticated as GitHub user: @{github_username} ({user_data.get('name')})")
    except urllib.error.HTTPError as e:
        print(f"[-] Authentication failed: HTTP {e.code} - {e.reason}")
        print("    Please verify that your Personal Access Token is valid and has 'repo' scope.")
        sys.exit(1)

    # 2. Check if repo exists or create it
    print(f"\n[2/4] Checking if repository '{repo_name}' exists on GitHub...")
    check_req = urllib.request.Request(
        f"https://api.github.com/repos/{github_username}/{repo_name}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "AgriVision-Setup"
        }
    )
    repo_exists = False
    try:
        with urllib.request.urlopen(check_req) as resp:
            repo_exists = True
            print(f"[+] Repository '{github_username}/{repo_name}' already exists on GitHub.")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"[*] Repository '{repo_name}' does not exist yet. Creating it now via GitHub API...")
            create_payload = json.dumps({
                "name": repo_name,
                "description": "AgriVision AI (TAH-015): Precision Agriculture and Crop Disease Predictor with PyTorch and FastAPI",
                "private": False,
                "has_issues": True,
                "has_projects": True,
                "has_wiki": True
            }).encode()

            create_req = urllib.request.Request(
                "https://api.github.com/user/repos",
                data=create_payload,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/vnd.github+json",
                    "User-Agent": "AgriVision-Setup",
                    "Content-Type": "application/json"
                }
            )
            try:
                with urllib.request.urlopen(create_req) as resp:
                    print(f"[+] Successfully created repository: https://github.com/{github_username}/{repo_name}")
            except Exception as create_err:
                print(f"[-] Failed to create repository: {create_err}")
                sys.exit(1)
        else:
            print(f"[-] Unexpected error checking repository: {e}")
            sys.exit(1)

    # 3. Configure remote and push
    print("\n[3/4] Preparing Git remote and branch...")
    remote_auth_url = f"https://{github_username}:{token}@github.com/{github_username}/{repo_name}.git"
    remote_clean_url = f"https://github.com/{github_username}/{repo_name}.git"

    # Set authenticated remote URL
    run_cmd(["git", "remote", "set-url", "origin", remote_auth_url], cwd=project_root)

    print("\n[4/4] Pushing commits to GitHub (branch: main)...")
    code, stdout, stderr = run_cmd(["git", "push", "-u", "origin", "main"], cwd=project_root)

    # Always sanitize remote URL immediately so tokens are never left in git config
    run_cmd(["git", "remote", "set-url", "origin", remote_clean_url], cwd=project_root)

    if code == 0:
        print("\n" + "="*50)
        print(f"[+] SUCCESS! AgriVision has been pushed to GitHub:")
        print(f"    https://github.com/{github_username}/{repo_name}")
        print("="*50)
    else:
        print(f"[-] Git push failed:\nSTDOUT: {stdout}\nSTDERR: {stderr}")
        sys.exit(1)

if __name__ == "__main__":
    main()
