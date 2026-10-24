"""txt 'name | strength | intent | why' -> data/<type>_scores.json; merges sima marks from data/<type>_sima.txt ('name | mark | note') if present."""
import json, sys, os
t = sys.argv[1]; base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
names = {f['name'] for f in json.load(open(f'{base}/{t}.json'))['factors']}
out = {}
for line in open(f'{base}/{t}_scores.txt'):
    if not line.strip(): continue
    n, s, i, w = [x.strip() for x in line.split('|', 3)]
    out[n] = dict(strength=int(s), intent=int(i), why=w, sima='?', sima_note='sima-land не проверена')
if os.path.exists(f'{base}/{t}_sima.txt'):
    for line in open(f'{base}/{t}_sima.txt'):
        if not line.strip(): continue
        n, m, *note = [x.strip() for x in line.split('|', 2)]
        assert n in out, n
        m = {'-': '–', '—': '–', '−': '–', '+/-': '±'}.get(m, m)
        assert m in ('+', '–', '±', '?'), (n, m)
        out[n]['sima'] = m; out[n]['sima_note'] = note[0] if note else ''
miss = names - out.keys(); extra = out.keys() - names
assert not miss and not extra, (miss, extra)
json.dump(out, open(f'{base}/{t}_scores.json', 'w'), ensure_ascii=False, indent=1)
print(t, len(out), 'ok')
