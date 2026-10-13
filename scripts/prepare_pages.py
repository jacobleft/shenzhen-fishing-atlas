"""检查报告链接并准备 Cloudflare Pages 静态文件。"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import shutil

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'outputs' / 'coastline-survey'
DIST = ROOT / '.pages-dist'

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = []
        self.refs = []
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.refs.append(attrs['href'])
        if tag == 'img' and 'src' in attrs:
            self.refs.append(attrs['src'])

pages = {p.name: Page(p) for p in SOURCE.glob('*.html')}
assert 'atlas.html' in pages, '缺少岸线图集首页'
for name, page in pages.items():
    assert len(page.ids) == len(set(page.ids)), f'{name} 有重复锚点'
    for ref in page.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc:
            continue
        filename = unquote(url.path) or name
        target = SOURCE / filename
        assert target.is_file(), f'{name} 链接缺失：{ref}'
        if url.fragment and filename in pages:
            assert unquote(url.fragment) in pages[filename].ids, f'{name} 锚点缺失：{ref}'
files = [p for p in SOURCE.iterdir() if p.is_file()]
assert len(files) + 3 <= 20000, '文件数量超过 Pages 免费套餐限制'
assert all(p.stat().st_size <= 25 * 1024 * 1024 for p in files), '存在超过25 MiB的文件'
if DIST.exists():
    shutil.rmtree(DIST)
shutil.copytree(SOURCE, DIST)
shutil.copyfile(SOURCE / 'atlas.html', DIST / 'index.html')
(DIST / '404.html').write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>页面不存在</title></head><body><main><h1>页面不存在</h1><p><a href="/atlas.html">岸线图集</a> · <a href="/topics.html">专题索引</a></p></main></body></html>', encoding='utf-8')
# HTML每次重新验证，图片保留较短缓存，更新同名影像时可刷新。
(DIST / '_headers').write_text('''/*.html
  Cache-Control: public, max-age=0, must-revalidate
/*.jpg
  Cache-Control: public, max-age=3600
/*.png
  Cache-Control: public, max-age=3600
''', encoding='utf-8')
print(f'已准备 {len(files) + 3} 个静态文件；{len(pages)} 个网页链接和锚点检查通过。')
