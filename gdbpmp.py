#!/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2012 Mak Nazečić-Andrlon
# Copyright (c) 2017 Mark Nelson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import os
import common
import gdbtypes
import subprocess
import signal
import time

def main():
    ctx = common.parse_args()
    if ctx.input:
        threads = common.load_threads(ctx.input)
        common.print_callgraph(threads)
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
