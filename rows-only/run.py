#!/usr/bin/env python

def portal_rows(portal, output_dir = 'rows', input_dir = 'data'):
    'Download all of the rows for one portal.'
    import os
    from urllib import urlretrieve

    portal_dir = os.path.join(output_dir, portal)
    try:
        os.makedirs(portal_dir)
    except OSError:
        pass

    for viewid_raw in open(os.path.join(input_dir, portal, 'viewids')).readlines():
        viewid = viewid_raw[:-1]
        output_file = os.path.join(portal_dir, viewid)
        if not os.path.exists(output_file):
            url = 'http://%s/api/views/%s/rows.csv?accessType=DOWNLOAD' % (portal, viewid)
            try:
                urlretrieve(url, filename = output_file)
            except:
                return (1, url)
    return (0,)

import os

def clear_empty():
    'Delete empty files'
    for portal in os.listdir('rows'):
        for viewid in os.listdir(os.path.join('rows', portal)):
            filename = os.path.join('rows', portal, viewid)
            if os.path.getsize(filename) == 0:
                os.remove(filename)

def parallel():
    nprocesses = 35
    from multiprocessing import Pool
    p = Pool(nprocesses)
    print p.map(portal_rows, os.listdir('data'))

def series():
    print map(portal_rows, os.listdir('data'))

if __name__ == '__main__':
    if 'http_proxy' not in os.environ:
        raise UserWarning('No http_proxy is set.')
    clear_empty()
    parallel()
