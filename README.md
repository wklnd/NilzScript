# NilzScript
## A mix of scripts I use
---
# Notes Syncer

A minimal Python script to sync a local notes folder with a GitHub repository using Git.

## Prerequisites
- Git installed and configured (SSH or HTTPS auth)
- Python 3.8+ on macOS
- Network access to the remote repository

## Configuration
Edit the constants at the top of `syncer.py` if needed:
- `REPO_URL`: Remote repository URL
- `LOCAL_DIR`: Local notes folder
- `BRANCH`: Git branch to use (default `main`)

## Setup
Clone and configure the repository locally:
```bash
python3 syncer.py install
```
This clones to `LOCAL_DIR` and sets `pull.rebase=true` and `rebase.autoStash=true`.

## Usage
Upload local changes to the remote (skips if no local edits):
```bash
python3 syncer.py upload 
```

Download latest changes from the remote:
```bash
python3 syncer.py download
```

Count total commits in the repository:
```bash
python3 syncer.py count
```
## Notes
- Upload uses rebase-based pulls and auto-stash to avoid merge commits.
- The repository is cloned into `LOCAL_DIR`; ensure you have write access.

- Tip: Setup a Cronjob or launchd for this script so the files are automatically synced. 

---
