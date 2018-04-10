#!/usr/bin/python

'''
Copyright (c) 2012-2016     Bob Copeland <me@bobcopeland.com>

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
'''

"""
This script is similar in output to parse.c from the radiotap-library
project and can be used to test the python library against its test
cases.
"""

import radiotap as r
import sys

fields_to_print = {
    'TSFT': [ 'TSFT', lambda x : x ],
    'flags': [ 'flags', lambda x : '%x' % x ],
    'rate': [ 'rate', lambda x : '%f' % x ],
    'rx_flags': [ 'RX flags', lambda x: '%0.4x' % x ]
}

def datastr(data, sep):
    return sep.join('%.2x' % ord(k) for k in data)

def print_vendor(row):
    """ Print vendor lines that match what parse.c does
    """
    data = row['data']
    oui = row['oui']

    if ((row['present'] & (1 << 0)) or
        (row['present'] & (1 << 52))):

        bit = 0 if (row['present'] & (1 << 0)) else 52
        print '\t%s-%.2x|%d: %s' % (
             datastr(oui, ':'), row['subns'], bit, datastr(data, '/'))
    elif row['subns'] != 0:
        print '\tvendor NS (%s:%d, %d bytes)\n\t\t%s' % (
             datastr(oui, '-'), row['subns'], len(data),
             datastr(data, ' '))

def parse_file(fn):
    pkt = open(fn).read()

    while len(pkt):
        off, radiotap = r.radiotap_parse(pkt, valuelist=True)
        for row in radiotap:
            if 'oui' in row:
                print_vendor(row)
            for k,v in row.items():
                if k in fields_to_print:
                    lbl, fmt = fields_to_print[k]
                    print '\t%s: %s' % (lbl, fmt(v))
        pkt = pkt[off:]

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "Usage: %s [file]" % sys.argv[0]
        sys.exit(1)

    parse_file(sys.argv[1])

