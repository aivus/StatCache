StatCache
=========

Implementation of [StatCache model](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.96.8725&rep=rep1&type=pdf) on Python

Usage: `python main.py access_file.mtr`


Access file
-----------

Access file should have next structure:

`<operation type> <size of block> <address>`

where:

`<operation type>` - type of operation: `l` (load) or `s` (store)

`<size of block>` - size of requested block

`<address>` - address of requested block

Example of access file:

    s 4 2147450736
    s 4 2147450748
    s 4 2147450744
    s 4 2147450740
    l 4 2147450780
    l 4 2147450776
    l 4 2147450772
    l 4 2147450768
    l 4 2147450800
