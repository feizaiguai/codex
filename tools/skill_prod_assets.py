import json
from pathlib import Path
from datetime import datetime
import re

root = Path(r'C:\\Users\\bigbao\\.codex\\skills')
out_dir = root / 'reports' / 'skills-prod-real' / '_inputs'
out_dir.mkdir(parents=True, exist_ok=True)

# Accessibility HTML from real README
readme_path = root / '01-spec-explorer-G' / 'README.md'
readme_text = readme_path.read_text(encoding='utf-8', errors='replace')
html = f"<html><body><h1>Spec Explorer</h1><pre>{readme_text}</pre></body></html>"
(out_dir / 'accessibility.html').write_text(html, encoding='utf-8')

# Log file with real timestamps and file stats
log_lines = []
now = datetime.utcnow().isoformat() + 'Z'
log_lines.append(f"{now} INFO system start")
for p in [root / '05-code-review-G' / 'handler.py', root / '04-test-automation-G' / 'handler.py']:
    size = p.stat().st_size
    log_lines.append(f"{now} INFO file {p.name} size={size}")
log_lines.append(f"{now} ERROR sample error code=E001")
(out_dir / 'app.log').write_text("\n".join(log_lines), encoding='utf-8')

# Explainability CSV with real file stats
files = [
    root / '05-code-review-G' / 'handler.py',
    root / '04-test-automation-G' / 'handler.py',
    root / '14-weibo-trending-G' / 'handler.py',
]
rows = []
for p in files:
    text = p.read_text(encoding='utf-8', errors='replace')
    rows.append({
        'file': p.name,
        'size': p.stat().st_size,
        'lines': len(text.splitlines()),
    })

csv_path = out_dir / 'explain.csv'
with csv_path.open('w', encoding='utf-8', newline='') as f:
    f.write('file,size,lines\n')
    for r in rows:
        f.write(f"{r['file']},{r['size']},{r['lines']}\n")

# Risk metrics from real code
code_path = root / '05-code-review-G' / 'engine.py'
code_text = code_path.read_text(encoding='utf-8', errors='replace')
complexity = len(re.findall(r'\bfor\b|\bwhile\b', code_text))
vulns = len(re.findall(r'TODO|FIXME', code_text))
metrics = {
    'complexity': complexity,
    'vulns': vulns,
    'lines': len(code_text.splitlines()),
}
(out_dir / 'risk_metrics.json').write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')

# Deps list from existing requirements
req_path = root / '37-chrome-automation-G' / 'requirements.txt'
if req_path.exists():
    deps = [line.strip() for line in req_path.read_text(encoding='utf-8', errors='replace').splitlines() if line.strip()]
else:
    deps = []
(out_dir / 'deps.txt').write_text("\n".join(deps), encoding='utf-8')

print(f"Assets created in {out_dir}")