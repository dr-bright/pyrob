"""Miscellaneous classes and functions"""

import itertools
import os, sys, csv
import matplotlib.pyplot as plt



def imshow(img, ax=None):
    if ax is None:
        fig, ax = plt.subplots()


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


def expand_glob(*files):
    files = [*files]
    for _ in range(len(files)):
        file = files.pop(0)
        files += glob(file)
    return files
# end

