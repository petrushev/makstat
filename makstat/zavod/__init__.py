from itertools import product, izip, tee
from collections import OrderedDict
import json


def get_metadata(stream):
    """Gets metadata from .px stream"""
    metadata = OrderedDict()

    full_line = ''
    for line in stream:
        if line.startswith('DATA'):
            # final entry
            linedata = full_line.split('=')
            key = linedata.pop(0)
            val = '='.join(linedata)
            if key != '':
                val = val.rstrip(';')
                metadata[key] = val
            break

        if '=' not in line:
            # line continued
            full_line = full_line + ' ' + line
            continue

        else:
            linedata = full_line.split('=')
            key = linedata.pop(0)
            val = '='.join(linedata)
            if key != '':
                val = val.rstrip(';')
                metadata[key] = val
            full_line = line

    return metadata

def get_dimensions(metadata):
    """Parse dimensions and their values from provided metadata"""
    dimensions = OrderedDict()
    for key, val in metadata.iteritems():
        if key.startswith('VALUES('):
            dim_key = key[8:-2]
            vals = val[1:-1].replace(', "', ',"').split('","')
            dimensions[dim_key] = vals

    return dimensions

def iter_atom_data(stream):
    """Yields single value of data"""
    for line in stream:
        if line.startswith('DATA='):
            break
    for line in stream:
        data = line.rstrip(' ;').split(' ')
        for atom in data:
            yield atom

def iter_contextual_atom_data(stream):
    """Iterates through data, providing context via dictionary with dimensions
    and their current values"""
    content, content_meta = tee(stream)
    metadata = get_metadata(content_meta)
    dims = get_dimensions(metadata)
    columns = dims.keys()

    idims = product(*dims.values())
    idata = iter_atom_data(content)

    for combined_dim_vals, atom in izip(idims, idata):
        data = dict(zip(columns, combined_dim_vals))
        data['value'] = atom
        yield data
