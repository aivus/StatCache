# coding=utf-8
import math

__author__ = 'Ilya Antipenko'


class StatCache(object):
    cache_line_size = -1;

    # Size of cache in lines
    cache_size = -1

    access_file = None
    histogram_file = None


    def _f(self, n):
        return 1 - pow(1 - (1 / self.cache_size), n)
        pass

    def _solve(self, curr_prob, hist, inst_count, cold_prob=False):
        if not cold_prob:
            sum = 0
        else:
            sum = inst_count * cold_prob

        for dist in hist:
            sum += hist[dist] * self.f(dist * curr_prob)

        return sum / inst_count

    def analyse(self):
        # TODO
        rates = dict()
        hist_index = dict()

        hist = dict()  # Histogram
        used_blocks = dict()  # Used blocks. For calculate reuse distance
        current_line = 0  # Current line
        cold_numbers = 0  # Numbers of "cold" misses

        for line in self.access_file:
            current_line += 1
            assert isinstance(line, str)
            inst_type, inst_size, inst_addr = line.split(" ")

            # Get number of used block
            block = math.floor(inst_addr / self.cache_line_size)
            offset = inst_addr % self.cache_line_size

            active_blocks = (block,)
            cur_block = block
            cur_size = inst_size

            while (offset + cur_size) > self.cache_line_size:
                # TODO: Need check it.
                # TODO: $active_blocks[] = ++$cur_block;
                cur_block += 1
                active_blocks += (cur_block,)
                cur_size -= self.cache_line_size

            for active_block_key in active_blocks:
                active_block_value = active_blocks[active_block_key]
                if active_block_value in used_blocks:
                    # Already
                    reuse_distance = current_line - used_blocks[active_block_value] - 1
                    if reuse_distance not in hist:
                        hist[reuse_distance] = 1
                    else:
                        hist[reuse_distance] += 1
                else:
                    # Cold miss
                    if active_block_value not in hist_index:
                        hist_index[active_block_value] = True
                        cold_numbers += 1

                used_blocks[active_block_value] = current_line

            # TODO: Strange check here
            if current_line > 0 and current_line % 200000 == 0:
                print "Strange check!"
                current_line += 1
                break

        insn_count = current_line


    def __init__(self, cache_line_size, cache_size, access_file, histogram_file):
        self.cache_line_size = cache_line_size
        self.cache_size = cache_size
        self.access_file = access_file
        self.histogram_file = histogram_file



