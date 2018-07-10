#!/usr/bin/env python3
# Copyright (c) 2017 Mark Nelson

import sys
import os

try:
    import common
except ImportError:
    sys.path.append(os.path.dirname(__file__))
    import common

import gdbtypes
import subprocess
import signal
import time

def main():
    ctx = common.parse_args()
    if ctx.input:
        threads = common.load_threads(ctx.input)
        common.print_callgraph(threads, ctx.threshold)
    elif ctx.pid:
        this_path = os.path.realpath(__file__)
        pargs = ' '.join(sys.argv[1:])

        args = [ctx.gdb_path, "-q", "--ex", "source %s" % this_path, "--ex",  "gdbpmp %s" % pargs]
        proc = subprocess.Popen(args)

        try:
            while proc.poll() is None:
                time.sleep(0.1) 
          
        except KeyboardInterrupt:
            proc.send_signal(signal.SIGINT)
            while proc.poll() is None:
                time.sleep(0.1)

if __name__ == "__main__":
    try:
        import tracer
    except ImportError:
        main()
        sys.exit(0)
    tracer.ProfileCommand()
