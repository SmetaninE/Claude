"""Replaces {{type:factor}} in a markdown template with competitor coverage 'k/n' from data/<type>.json."""
import json, re, sys, os
base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
cache = {}
def cov(m):
    t, name = m.group(1), m.group(2)
    if t not in cache: cache[t] = json.load(open(f'{base}/{t}.json'))
    d = cache[t]
    live = [u['domain'] for u in d['urls'] if u['status'].startswith(('ok', 'частично'))]
    f = next((f for f in d['factors'] if f['name'] == name), None)
    if f is None: sys.exit(f'unknown factor {t}:{name}')
    k = sum(f['marks'].get(x) == '+' for x in live); q = sum(f['marks'].get(x) == '?' for x in live)
    return f'{k}/{len(live)}' + (f' (+{q} «?»)' if q else '')
src, dst = sys.argv[1], sys.argv[2]
open(dst, 'w').write(re.sub(r'\{\{(\w+):(.+?)\}\}', cov, open(src).read()))
