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

# index names and values
data = {}
values = []
indexcols = []

for cur_data in iter_contextual_atom_data(stream):
    for k, v in cur_data.iteritems():
        if k == 'value':
            values.append(v)
        else:
            k_enc = k
            if k_enc not in indexcols:
                indexcols.append(k_enc)
                data[k_enc] = []
            data[k_enc].append(v)

data[title] = values

df = DataFrame(data)
df.set_index(indexcols, inplace=True)

# create removable temp file for use with HDFStore
tmpfile = NamedTemporaryFile().name

store = HDFStore(tmpfile)
store['default'] = df
store.close()

# put h5 file to stdout
with open(tmpfile, 'rb') as f:
    print f.read()

# temp file is automatically removed
