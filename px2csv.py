from sys import stdin

from pandas.core.frame import DataFrame

from makstat.zavod import iter_contextual_atom_data

stream = (line.decode('cp1251').strip().encode('utf-8')
          for line in stdin)

df = DataFrame()
for cur_data in iter_contextual_atom_data(stream):
    current = DataFrame.from_dict([cur_data])
    df = df.append(current, ignore_index=False)

print df.to_csv(index=False, quotechar="\"", escapechar="\\")
