#!/usr/bin/env python3
"""Check public docs, including links to the repository's SLAM source notes."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from html.parser import HTMLParser
import re, sys

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
SOURCES = ROOT / 'SLAM'

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.targets = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('href','src') and value:
                self.targets.append((value, key == 'src'))

def plain(text):
    return re.sub(r'^(`{3,}|~{3,}).*?^\1\s*$', '', text, flags=re.M|re.S)

def anchors(path):
    text = plain(path.read_text())
    result, counts = set(), {}
    for heading in re.findall(r'^#{1,6}\s+(.+)$',text,re.M):
        name = re.sub(r'<[^>]*>','',heading).strip().lower()
        name = re.sub(r'[^\w\-\s]','',name)
        name = re.sub(r'\s','-',name)
        idx = counts.get(name,0); counts[name] = idx+1
        result.add(name if idx==0 else f'{name}-{idx}')
    return result

def check():
    errors, checked = [], 0
    for page in sorted(DOCS.rglob('*.md')):
        text = plain(page.read_text())
        if '[[' in text:
            errors.append(f'{page.relative_to(ROOT)}: unresolved Obsidian link')
        if not re.search(r'^#\s+',text,re.M):
            errors.append(f'{page.relative_to(ROOT)}: missing page title')
        html = Links(); html.feed(text)
        targets = [(link, bool(image)) for image, link in
                   re.findall(r'(!?)\[[^\]\n]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)',text)]
        targets += html.targets
        cover = re.search(r'^cover:\s*(\S+)',text,re.M)
        if cover: targets.append((cover.group(1), True))
        for link, is_image in targets:
            if link.startswith(('http:','https:','mailto:','tel:','data:','/files/','/pages/')):
                continue
            split=urlsplit(link); local=unquote(split.path)
            target=(page.parent/local).resolve() if local else page.resolve()
            checked+=1
            source_link = (not is_image and target.is_relative_to(ROOT.resolve())
                           and target.is_relative_to(SOURCES.resolve()))
            anchor_page = target / 'README.md' if target.is_dir() else target
            if not target.is_relative_to(DOCS.resolve()) and not source_link:
                errors.append(f'{page.relative_to(ROOT)}: link leaves docs: {link}')
            elif not target.exists():
                errors.append(f'{page.relative_to(ROOT)}: missing target: {link}')
            elif (split.fragment and anchor_page.is_file() and anchor_page.suffix=='.md'
                  and unquote(split.fragment) not in anchors(anchor_page)):
                errors.append(f'{page.relative_to(ROOT)}: missing anchor: {link}')
    summary=(DOCS/'SUMMARY.md').read_text()
    entries=re.findall(r'\[[^\]]+\]\(([^)]+)\)',summary)
    if len(entries)!=len(set(entries)):
        errors.append('docs/SUMMARY.md: duplicate navigation target')
    for path in DOCS.rglob('*.md'):
        rel=path.relative_to(DOCS).as_posix()
        if rel!='SUMMARY.md' and rel not in entries:
            errors.append(f'docs/{rel}: not included in navigation')
    if errors:
        print('\n'.join(errors)); return 1
    print(f'OK: {len(entries)} pages, {checked} local references, navigation and anchors valid')
    return 0

if __name__=='__main__':
    sys.exit(check())
