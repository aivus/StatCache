# coding=utf-8
from __future__ import division
import math

__author__ = 'Ilya Antipenko'


class StatCache(object):
    cache_line_size = None

    # Size of cache in lines
    cache_size = None

    access_file = None

    def _f(self, n):
        return 1 - pow(1 - (1 / self.cache_size), n)
        pass

    def _solve(self, curr_prob, hist, inst_count, cold_prob=None):
        if cold_prob is None:
            sum = 0
        else:
            sum = inst_count * cold_prob

        for dist in hist:
            sum += hist[dist] * self._f(dist * curr_prob)

        return sum / inst_count

    def analyse(self):
        caches = dict()
        cold_miss_index = dict()

        hist = dict()  # Histogram
        used_blocks = dict()  # Used blocks. For calculate reuse distance
        current_line = 0  # Current line
        cold_numbers = 0  # Numbers of "cold" misses

        for line in self.access_file:
            current_line += 1
            assert isinstance(line, str)
            inst_type, inst_size, inst_addr = line.split(" ")

            inst_size = int(inst_size)
            inst_addr = int(inst_addr)

            # Get number of used block
            block = math.floor(inst_addr / self.cache_line_size)
            offset = inst_addr % self.cache_line_size

            active_blocks = (block,)
            cur_block = block
            cur_size = inst_size

            while (offset + cur_size) > self.cache_line_size:
                cur_block += 1
                active_blocks += (cur_block,)
                cur_size -= self.cache_line_size

            for active_block_value in active_blocks:
                if active_block_value in used_blocks:
                    # Already
                    reuse_distance = current_line - used_blocks[active_block_value] - 1
                    if reuse_distance not in hist:
                        hist[reuse_distance] = 1
                    else:
                        hist[reuse_distance] += 1
                else:
                    # Cold miss
                    if active_block_value not in cold_miss_index:
                        cold_miss_index[active_block_value] = True
                        cold_numbers += 1

                used_blocks[active_block_value] = current_line

        insn_count = current_line

        for cur_k_size in custom_xrange(1, 1024, lambda x: x * 2):
            self.cache_size = cur_k_size * 1024 / self.cache_line_size
            cold_prob = cold_numbers / insn_count
            prob = 0.5
            eps = 0.0001
            while True:
                prob_prev = prob
                prob = self._solve(prob, hist, insn_count, cold_prob)
                if abs(prob_prev - prob) < eps:
                    break

            caches[cur_k_size] = prob

        for cache in sorted(caches):
            print "%d %f" % (cache, caches[cache])

    def __init__(self, cache_line_size, access_file):
        self.cache_line_size = cache_line_size
        self.access_file = access_file


def custom_xrange(start, stop, step_callback):
    current = start
    while current <= stop:
        yield current
        current = step_callback(current)
