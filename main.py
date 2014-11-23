import sys
from StatCache import StatCache

__author__ = 'Ilya Antipenko'

cache_line_size = 8
cache_size = 1024 * 1024 / cache_line_size

def main():
    if len(sys.argv) != 3:
        print "Incorrect count of arguments. Expected: %d. Actual: %d" % (3, len(sys.argv))
        exit(1)
    try:
        access_file = open(sys.argv[1], 'r')
    except IOError:
        print "Can't open access memory file: %s" % sys.argv[1]
        exit(2)

    try:
        histogram_file = open(sys.argv[2], 'w+')
    except IOError:
        print "Can't create histogram file: %s" % sys.argv[2]
        exit(3)

    stat_cache = StatCache(cache_line_size, cache_size, access_file, histogram_file)
    stat_cache.analyse()

    access_file.close()
    histogram_file.close()


if __name__ == '__main__':
    main()
