import sys
import time
from StatCache import StatCache

__author__ = 'Ilya Antipenko'

expected_count_of_args = 2

cache_line_size = 8


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2 - time1) * 1000.0)
        return ret

    return wrap


def print_error(message):
    print >> sys.stderr, message


@timing
def main():
    if len(sys.argv) != expected_count_of_args:
        print_error("Error! Incorrect count of arguments. Expected: %d. Actual: %d" %
                    (expected_count_of_args, len(sys.argv)))
        print_error("Usage: %s access_log.mtr" % sys.argv[0])
        exit(1)

    try:
        access_file = open(sys.argv[1], 'r')
    except IOError:
        print "Can't open access memory file: %s" % sys.argv[1]
        exit(2)

    stat_cache = StatCache(cache_line_size, access_file)
    stat_cache.analyse()

    access_file.close()

if __name__ == '__main__':
    main()
