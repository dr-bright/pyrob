"""Miscellaneous classes and functions"""

import itertools
import os, sys, csv

try:
    import pandas as pd
    pandas_flag = True
except ImportError:
    pandas_flag = False


class text(str):
    """Indicates literal text at places where filepath is extected."""
    pass



def read_file(source, *, encode=None, decode=None, literal=None, seek0=True):
    """Read and decode data from *any* source.
    
    Args:
        source: str|text|bytes|readable   - str is path, text is literal
                                          - text is any str subclass
        encode:  If source is textual, encode data to bytes using this charset
        decode:  If source is binary, decode data from bytes with this charset
        literal: If True, treat all strings literally
        seek0:   If True and source is seekable, return to the original pos
    """
    if type(source) == str and not literal:
        if decode is not None:
            file = open(source, 'rt', encoding=decode)
        else:
            file = open(source, 'rb')
        with file as f:
            return f.read()
    elif isinstance(source, str):
        if encode is not None:
            return source.encode(encode)
        return source
    elif isinstance(source, bytes):
        if decode is not None:
            return source.decode(decode)
        return source
    elif seek0 and source.seekable():
        i = source.tell()
        rsp = source.read()
        source.seek(i)
        return rsp
    else:
        return source.read()


def write_file(data, dest, *, charset='utf-8', seek0=False):
    """Puts data into *any* dest.
    
    Args:
        data: bytes or str
        dest: str|writable
        charset: if data and dest type aren't same, reencode data with this charset
        seek0:   if true and if dest is seekable, return to the original pos
    """
    dest_type = 'bin'
    close = True
    if not isinstance(dest, str):
        close = False
        try:
            dest.write(b'')
        except:
            dest_type = 'txt'
    elif isinstance(data, str):
        dest = open(dest, 'wt', encoding=charset)
        dest_type = 'txt'
        seek0 = False
    else:
        dest = open(dest, 'wb')
        seek0 = False
    try:
        seek0 = seek0 and dest.seekable()
        if seek0:
            i = dest.tell()
        if isinstance(data, str) and dest_type == 'bin':
            rsp = dest.write(data.encode(charset))
        elif isinstance(data, bytes) and dest_type == 'txt':
            rsp = dest.write(data.decode(charset))
        else:
            rsp = dest.write(data)
        if seek0:
            dest.seek(i)
    finally:
        if close:
            dest.close()


def write_csv(data, *, file=None, sep=',', header=None, columns=None,
                       encoding='utf-8', seek0=False, **kwargs):
    """...
    
    data: str|dict|list[list]|list[dict]   - dict is single record
    columns: None | list[str] | list[int]  - these are actually displayed
    header: bool | list[str] | None        - header is aliases for all `columns`
    """
    if file is None:
        file = sys.stdout
    close = False
    if isinstance(file, str):
        close = True
    seek0 = seek0 and not close and file.seekable()
    if seek0:
        ipos = file.tell()
    if pandas_flag and isinstance(data, pd.DataFrame): # DataFrame
        try:
            if header is None:
                header = True
            data.to_csv(file, sep=sep, encoding=encoding,
                              header=header, index=False,
                **kwargs)
        finally:
            if seek0:
                file.seek(ipos)
        return
    if close:
        file = open(file, 'wt', encoding=encoding)
    writerow = csv.writer(file, delimiter=sep).writerow
    try:
        if hasattr(data, 'keys') and hasattr(data, '__getitem__'): # dict
            if header is None:
                header = True
            if columns is None:
                columns = [*data.keys()]
            if header is True:
                writerow(columns)
            elif header:
                writerow(header + columns[len(header):])
            writerow(data[k] for k in columns)
            return
        data = iter(data)
        try:
            row0 = next(data)
        except StopIteration:
            return
        if hasattr(row0, 'keys') and hasattr(row0, '__getitem__'): # list[dict]
            if header is None:
                header = True
            if columns is None:
                columns = [*row0.keys()]
            if header is True:
                writerow(columns)
            elif header:
                writerow(header + columns[len(header):])
            for record in itertools.chain([row0], data):
                values = (record[k] for k in columns)
                writerow(values)
        else:                                                       # list[list]
            if header is None:
                header = False
            if header is True:
                if columns is not None:
                    header = columns
                else:
                    row0 = list(row0)
                    header = range(len(row0))
            if header:
                writerow(header)
            for record in itertools.chain([row0], data):
                values = (val for i, val in enumerate(record)
                              if not columns or i in columns
                         )
                writerow(values)
    finally:
        if seek0:
            file.seek(ipos)
        if close:
            file.close()
    return


def safe_wx(filepath, suffix=" ({0})", encoding=None):
    """Open file with open(path, 'x'), retry with suffix if failed."""
    mode = 'xb' if encoding else 'xt'
    i = 2
    base, ext = os.path.splitext(filepath)
    while True:
        try:
            return open(filepath, mode, encoding=encoding)
        except FileExistsError:
            filepath = base + suffix.format(i) + ext
            i += 1


def expand_glob(*files):
    files = [*files]
    for _ in range(len(files)):
        file = files.pop(0)
        files += glob(file)
    return files
# end

