"""Write MANIFEST.csv (path, bytes, sha256) for the reproduction set."""
import csv, glob, hashlib, os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
tracked = set(subprocess.run(["git", "ls-files", "."], capture_output=True, text=True, check=True).stdout.split())
pats = ["analysis/*.py", "analysis/*.json", "tables/*", "figures/*", "data/processed/*", "cache/*.json", "DATA_SOURCE_AUDIT.md", "requirements.txt", "LICENSE", "README.md", "tests/*.py"]
paths = sorted({p for pat in pats for p in glob.glob(pat) if os.path.isfile(p) and (p in tracked or not p.startswith(("data/", "cache/")))})
with open("MANIFEST.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["path", "bytes", "sha256"])
    for p in paths:
        b = open(p, "rb").read(); w.writerow([p, len(b), hashlib.sha256(b).hexdigest()])
print(f"MANIFEST.csv: {len(paths)} files")
