import json,sys
d=json.load(open(sys.argv[1]));print(d['intent'])
live=[u['domain'] for u in d['urls'] if u['status'].startswith(('ok','част'))];print(live)
for f in d['factors']:
  k=sum(f['marks'].get(x)=='+' for x in live);q=sum(f['marks'].get(x)=='?' for x in live)
  print(f"{k}{'/'+str(q)+'?' if q else ''} | {f['name']} | {f['group'][:5]} | {f['description'][:75]}")
