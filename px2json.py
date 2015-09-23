from sys import stdin
import json
from makstat.zavod import iter_contextual_atom_data

stream = (line.decode('cp1251').strip()
          for line in stdin)

for data in iter_contextual_atom_data(stream):
    print json.dumps(data)
