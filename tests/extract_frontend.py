from pathlib import Path
import re

html = Path("index.html").read_text(encoding="utf-8")
scripts = re.findall(r"<script>(.*?)</script>", html, flags=re.DOTALL)
if len(scripts) != 1:
    raise SystemExit(f"Expected one inline application script, found {len(scripts)}")
Path("/tmp/ironhaven-frontend.js").write_text(scripts[0], encoding="utf-8")
print("Extracted Ironhaven frontend script for syntax validation.")
