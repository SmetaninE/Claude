"""Usage: python3 -I extract.py <html_file> [url]  -> prints JSON with technical/structural facts."""
import sys, json, re
from bs4 import BeautifulSoup

def txt(e, n=200):
    return re.sub(r'\s+', ' ', e.get_text(' ', strip=True))[:n] if e else None

def jsonld_types(obj, out):
    if isinstance(obj, dict):
        t = obj.get('@type')
        if t: out.extend(t if isinstance(t, list) else [t])
        for v in obj.values(): jsonld_types(v, out)
    elif isinstance(obj, list):
        for v in obj: jsonld_types(v, out)

def main(path, url=None):
    raw = open(path, 'rb').read()
    s = BeautifulSoup(raw, 'lxml')
    meta = lambda **kw: (s.find('meta', attrs=kw) or {}).get('content')
    canon = s.find('link', rel='canonical')
    ld_types, ld_err = [], 0
    for sc in s.find_all('script', type='application/ld+json'):
        try: jsonld_types(json.loads(sc.string or ''), ld_types)
        except Exception: ld_err += 1
    micro = sorted({i.get('itemtype', '').split('/')[-1] for i in s.find_all(attrs={'itemtype': True})})
    bc = s.select('[class*="breadcrumb" i], nav[aria-label*="bread" i], [itemtype*="BreadcrumbList"]')
    body_text = txt(s.body, 10**7) or ''
    res = {
        'url': url, 'bytes': len(raw),
        'title': txt(s.title), 'description': meta(name='description'),
        'keywords_meta': meta(name='keywords'), 'robots': meta(name='robots'),
        'canonical': canon.get('href') if canon else None,
        'og': {m['property']: m.get('content', '')[:120] for m in s.find_all('meta', property=re.compile('^og:'))},
        'twitter_card': bool(s.find('meta', attrs={'name': re.compile('^twitter:')})),
        'hreflang': [l.get('hreflang') for l in s.find_all('link', hreflang=True)],
        'h1': [txt(h) for h in s.find_all('h1')],
        'h2': [txt(h, 120) for h in s.find_all('h2')][:60],
        'h3': [txt(h, 120) for h in s.find_all('h3')][:80],
        'jsonld_types': sorted(set(ld_types)), 'jsonld_parse_errors': ld_err,
        'microdata_types': micro,
        'breadcrumbs': txt(bc[0], 300) if bc else None,
        'text_len': len(body_text),
        'links_total': len(s.find_all('a', href=True)),
        'imgs': len(s.find_all('img')), 'imgs_with_alt': len([i for i in s.find_all('img') if i.get('alt')]),
        'forms': len(s.find_all('form')), 'iframes': [i.get('src', '')[:80] for i in s.find_all('iframe')][:10],
        'videos': len(s.find_all('video')),
        'scripts': len(s.find_all('script')),
        'antibot_hint': bool(re.search(r'captcha|антибот|checking your browser|Доступ ограничен|smartcaptcha|cf-chl|ddos-guard|__qrator|incapsula|Почти готово', raw.decode('utf-8', 'ignore'), re.I)),
    }
    print(json.dumps(res, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
