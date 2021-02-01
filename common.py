#!/usr/bin/env python3
# Copyright (c) 2017 Mark Nelson

import argparse
import pickle
from gdbtypes import GDBFunction, GDBThread

def parse_args(args=None):
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--input', required=False, type=str, help='Read collected samples from this file.')
    group.add_argument('-p', '--pid', required=False, type=int, help='PID of the process to connect to.')

    parser.add_argument('-s', '--sleep', required=False, type=float, default=0.01, help='Period of time to sleep between samples in seconds.')
    parser.add_argument('-n', '--samples', required=False, type=int, default=1000, help='The number of samples to collect.')
    parser.add_argument('-m', '--match', required=False, type=str, help='A comma separated list of strings to match with threads')
    parser.add_argument('-x', '--exclude', required=False, type=str, help='A comma separated list of strings to match when excluding threads.')
    parser.add_argument('-o', '--output', required=False, type=str, help='Write collected samples to this file.')
    parser.add_argument('-g', '--gdb_path', required=False, type=str, default='/usr/bin/gdb', help='Path to the GDB executable.')
    parser.add_argument('-t', '--threshold', required=False, type=float, default=0.1, help='Ignore results below the threshold when making the callgraph.')
    parser.add_argument('-v', '--invert', required=False, action='store_true', help='Print inverted callgraph.')
    if args:
        return parser.parse_args(args)
    else:
        return parser.parse_args()

def print_callgraph(threads, threshold):
    print("");
    for thn, gdbth in sorted(threads.items()):
        samples = gdbth.function.get_samples(True)
        print("")
        print(("Thread: %s (%s) - %s samples " % (gdbth.num, gdbth.name, samples)))
        print("")
        gdbth.function.print_percent("", samples, threshold, True)

def print_inverted_callgraph(threads, threshold):
    print("")
    for thn, gdbth in sorted(threads.items()):
        samples = gdbth.function.get_samples(True)
        igdbth = invert_thread(gdbth) 
        print("")
        print(("Thread: %s (%s) - %s samples " % (igdbth.num, igdbth.name, samples)))
        print("")
        igdbth.function.print_percent("", samples, threshold, False)

def invert_thread(gdbth):
    inverted_func = GDBFunction(None, 2)
    invert_function(gdbth.function, inverted_func)
    return GDBThread(gdbth.name, gdbth.num, gdbth.ptid, inverted_func)

def invert_function(input_func, base_func):
    ret = []

    # If we spent time directly in this function, add it to the base_func
    if input_func.count > 0:
        func = base_func.get_or_add_func(input_func.name)
        func.count += input_func.count
        ret.append((func, input_func.count))

    # iterate over the subfunctions
    for subfunction in input_func.subfunctions:
        tree_funcs = invert_function(subfunction, base_func)

        for (tree_func, count) in tree_funcs:
            func = tree_func.get_or_add_func(input_func.name)
            func.count += count
            ret.append((func, count))

    return ret

def dump_threads(threads, filename):
    with open(filename, 'wb') as handle:
        pickle.dump(threads, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_threads(filename):
    with open(filename, 'rb') as handle:
        return pickle.load(handle)
