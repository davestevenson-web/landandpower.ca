#!/usr/bin/env python3
"""Build the in-chat preview widget HTML for the Land and Power site.

Embeds brand images as data URIs and appends a dark-theme override block.
The override block is preview-only: the live site CSS (styles.css) is untouched.
Run:  python3 build-preview.py   -> writes .preview-widget.html
"""
import base64
import io
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent

DARK = """
/* ---------- In-chat dark-theme preview support (preview only) ---------- */
html[data-theme="dark"] {
  --ink: #e9f1ea;
  --muted: #a9bcae;
  --bg: #0f1a13;
  --bg-alt: #142019;
  --line: #26402e;
  --green-deep: #8fd0a4;
  --shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}
html[data-theme="dark"] .nav { background: rgba(15, 26, 19, 0.94); }
html[data-theme="dark"] .brand-text { color: #8fd0a4; }
html[data-theme="dark"] .nav-links a { color: var(--ink); }
html[data-theme="dark"] .hero {
  background:
    radial-gradient(ellipse 65% 55% at 50% -5%, rgba(143, 208, 164, 0.08), transparent 70%),
    var(--bg);
}
html[data-theme="dark"] .card,
html[data-theme="dark"] .step,
html[data-theme="dark"] .about-card { background: #152219; }
html[data-theme="dark"] .card-icon { background: rgba(143, 208, 164, 0.14); color: #8fd0a4; }
html[data-theme="dark"] .kicker,
html[data-theme="dark"] .eyebrow,
html[data-theme="dark"] .hero-tagline,
html[data-theme="dark"] .step-num,
html[data-theme="dark"] .about-card .tagline { color: #e8a37e; }
html[data-theme="dark"] .kicker::before,
html[data-theme="dark"] .contact .kicker::before { background: #e8a37e; }
html[data-theme="dark"] .btn-outline { border-color: #8fd0a4; color: #8fd0a4; }
html[data-theme="dark"] .btn-outline:hover { background: #8fd0a4; color: #0f1a13; }
/* Keep the contact band in the brand deep green in dark theme */
html[data-theme="dark"] .contact { background: #013a1a; }
html[data-theme="dark"] .btn-light { color: #013a1a; }
html[data-theme="dark"] .faq-item:hover { background: rgba(143, 208, 164, 0.06); }
html[data-theme="dark"] .footer { color: rgba(255, 255, 255, 0.85); }
html[data-theme="dark"] .footer-tag { color: #e8a37e; }
html[data-theme="dark"] .hero-logo {
  background: #f2f6f2;
  border-radius: 28px;
  padding: 22px;
  width: 212px;
}
"""


def datauri(path: Path, width: int) -> str:
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    im = im.resize((width, int(h * width / w)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def main() -> None:
    emblem = datauri(ROOT / "assets/emblem.png", 640)
    tower = datauri(ROOT / "assets/tower.png", 640)
    mark = datauri(ROOT / "assets/mark.png", 144)
    html = (ROOT / "index.html").read_text()
    css = (ROOT / "styles.css").read_text()
    body = re.search(r"<body>(.*)</body>", html, re.S).group(1)
    body = body.replace('src="assets/emblem.png"', f'src="{emblem}"')
    body = body.replace('src="assets/tower.png"', f'src="{tower}"')
    body = body.replace('src="assets/mark.png"', f'src="{mark}"')
    widget = (
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"'
        ' rel="stylesheet">\n'
        "<style>\n" + css + DARK + "\n</style>\n" + body
    )
    out = ROOT / ".preview-widget.html"
    out.write_text(widget)
    print("widget bytes:", len(widget))


if __name__ == "__main__":
    main()
