"""Pack Vite's single-entry React build into one directly openable HTML file."""
from pathlib import Path
import re

root=Path(__file__).resolve().parents[1]
dist=root/'frontend/dist'
html=(dist/'index.html').read_text()
def script(match):
    source=match.group(1)
    body=(dist/source.lstrip('/')).read_text()
    # Do not allow a literal closing tag in the script's data/code to end it early.
    body=body.replace('</script', '<\\/script')
    return '<script type="module">'+body+'</script>'
def style(match):
    source=match.group(1)
    return '<style>'+(dist/source.lstrip('/')).read_text()+'</style>'
html=re.sub(r'<script[^>]*src="([^"]+)"[^>]*></script>',script,html)
html=re.sub(r'<link[^>]*rel="stylesheet"[^>]*href="([^"]+)"[^>]*>',style,html)
assert not re.search(r'<script[^>]+src=|<link[^>]+rel="stylesheet"',html)
(root/'index.html').write_text(html)
print(f'Packed {len(html.encode()):,} bytes: {root / "index.html"}')
