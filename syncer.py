import os
import subprocess
import argparse
from datetime import datetime

REPO_URL = "REPO_URL_HERE"
LOCAL_DIR = os.path.expanduser("~/FOLDER_HERE")
BRANCH = "main"


def run(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, check=True)


def repo_exists():
    return os.path.isdir(os.path.join(LOCAL_DIR, ".git"))


def clone_repo():
    print("Cloning repository...")
    run(["git", "clone", "-b", BRANCH, REPO_URL, LOCAL_DIR])
    run(["git", "config", "--local", "pull.rebase", "true"], cwd=LOCAL_DIR)
    run(["git", "config", "--local", "rebase.autoStash", "true"], cwd=LOCAL_DIR)


def ensure_repo():
    if not os.path.exists(LOCAL_DIR):
        clone_repo()
    elif not repo_exists():
        raise RuntimeError(f"{LOCAL_DIR} exists but is not a git repository")
    else:
        run(["git", "config", "--local", "pull.rebase", "true"], cwd=LOCAL_DIR)
        run(["git", "config", "--local", "rebase.autoStash", "true"], cwd=LOCAL_DIR)


def has_changes():
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=LOCAL_DIR,
        capture_output=True,
        text=True,
    )
    return bool(result.stdout.strip())


def upload_notes(message=None):
    ensure_repo()
    if not has_changes():
        print("No local edits detected; skipping upload.")
        return
    run(["git", "add", "-A"], cwd=LOCAL_DIR)
    if not message:
        date = datetime.now().strftime("%Y-%m-%d")
        message = f"AC - sync notes | {date}"
    run(["git", "commit", "-m", message], cwd=LOCAL_DIR)

    print("Pulling latest changes...")
    run(["git", "pull"], cwd=LOCAL_DIR)

    print("Pushing changes...")
    run(["git", "push", "origin", BRANCH], cwd=LOCAL_DIR)
    print("Upload complete.")


def download_notes():
    ensure_repo()
    print("Pulling latest changes...")
    run(["git", "pull", "--ff-only"], cwd=LOCAL_DIR)
    print("Download complete.")

def install():
    ensure_repo()
    print("Installation complete. Repository is set up at:", LOCAL_DIR)

def how_many_commits_in_repo():
    ensure_repo()
    result = subprocess.run(
        ["git", "rev-list", "--count", "HEAD"],
        cwd=LOCAL_DIR,
        capture_output=True,
        text=True,
    )
    count = int(result.stdout.strip())
    return count



def main():
    parser = argparse.ArgumentParser(description="Sync notes with git")
    parser.add_argument(
        "action",
        choices=["upload", "download", 
                 "install", "count"],
        help="Upload or download notes",
    )
    parser.add_argument(
        "-m",
        "--message",
        help="Commit message (upload only)",
    )

    args = parser.parse_args()

    if args.action == "upload":
        upload_notes(args.message)
    elif args.action == "download":
        download_notes()
    elif args.action == "install":
        install()
    elif args.action == "count":
        count = how_many_commits_in_repo()
        print(f"Total commits in repository: {count}")  


if __name__ == "__main__":
    main()
