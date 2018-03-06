#!/bin/python
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
    if args:
        return parser.parse_args(args)
    else:
        return parser.parse_args()

def print_callgraph(threads):
    print("");
    for thn, gdbth in sorted(threads.iteritems()):
       print("")
       print("Thread: %s (%s) - %s samples " % (gdbth.num, gdbth.name, gdbth.function.get_samples()))
       print("")
       gdbth.function.print_percent("", gdbth.function.get_samples())

def dump_threads(threads, filename):
    with open(filename, 'wb') as handle:
        pickle.dump(threads, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_threads(filename):
    with open(filename, 'rb') as handle:
        return pickle.load(handle)
