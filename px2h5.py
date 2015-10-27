from sys import stdin
from itertools import tee
from tempfile import NamedTemporaryFile

from pandas.core.frame import DataFrame
from pandas.io.pytables import HDFStore

from makstat.zavod import iter_contextual_atom_data, get_metadata


stream = (line.decode('cp1251').strip().encode('utf-8')
          for line in stdin)

# tee the stream to get the metadata for title
stream, stream_2 = tee(stream)

title = get_metadata(stream_2)['TITLE']

df = DataFrame()
for cur_data in iter_contextual_atom_data(stream):
    current = DataFrame.from_dict([cur_data])
    df = df.append(current, ignore_index=False)

index_cols = list(df.columns.values)
index_cols.remove('value')
df.set_index(index_cols, inplace=True)
df.columns = [title]

# create removable temp file for use with HDFStore
tmpfile = NamedTemporaryFile().name

store = HDFStore(tmpfile)
store['default'] = df
store.close()

# put h5 file to stdout
with open(tmpfile, 'rb') as f:
    print f.read()

# temp file is automatically removed
