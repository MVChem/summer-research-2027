"""Read public faculty pages for link and affiliation checks; no guessed identities."""
import csv
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader((ROOT / 'data/source_inputs/expansion_100.tsv').open(), delimiter='\t'))

def check(row):
    result = {'name': row['name'], 'url': row['homepage']}
    try:
        response = requests.get(row['homepage'], timeout=22, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        text = ' '.join(soup.stripped_strings)
        result.update(status=response.status_code, finalUrl=response.url,
                      title=soup.title.get_text(' ', strip=True) if soup.title else '',
                      nameFound=all(part.casefold() in text.casefold() for part in row['name'].replace('-', ' ').split()),
                      text=text[:55000])
    except requests.RequestException as exc:
        result['error'] = type(exc).__name__
    return result

with ThreadPoolExecutor(max_workers=16) as executor:
    results = list(executor.map(check, rows))
(ROOT / 'data/source_inputs/expansion_source_checks.json').write_text(json.dumps(results, ensure_ascii=False, indent=2))
for r in results:
    if r.get('status') != 200 or not r.get('nameFound'):
        print(r['name'], r.get('status', r.get('error')), r.get('title', '')[:100])
print('Checked', len(results), 'public pages')
