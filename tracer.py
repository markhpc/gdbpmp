#!/usr/bin/env python3
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

from time import sleep
import gdb
import os
import signal
import pickle
import common
from gdbtypes import GDBThread, GDBFunction

class ProfileCommand(gdb.Command):
    def __init__(self):
        super(ProfileCommand, self).__init__("gdbpmp",
                                              gdb.COMMAND_RUNNING, gdb.COMPLETE_NONE, True)
        self.threads = {}
        
    def invoke(self, argument, from_tty):
        detatch_and_kill = 0
        self.dont_repeat()
        ctx = common.parse_args(gdb.string_to_argv(argument))
        if ctx.input:
            threads = common.load_threads(ctx.input)
            common.print_callgraph(threads) 
            return

        gdb.execute("set print thread-events off")
        gdb.execute("set print inferior-events off")
        gdb.execute("set pagination off")

        if ctx.pid and  ctx.pid != gdb.selected_inferior().pid:
            detach_and_kill = 1 
            gdb.write("Attaching to process %d..." % ctx.pid)
            gdb.flush(gdb.STDOUT)
            if gdb.selected_inferior().pid != 0:
                gdb.execute("detach", to_string=True)
            os.kill(ctx.pid, signal.SIGSTOP)
            gdb.execute("attach %d" % ctx.pid, to_string=True)
            os.kill(ctx.pid, signal.SIGCONT) 
            gdb.execute("continue", to_string=True)
            gdb.write("Done.\n")
            gdb.flush(gdb.STDOUT)
        def breaking_continue_handler(event):
            sleep(ctx.sleep)
            os.kill(gdb.selected_inferior().pid, signal.SIGINT)

        samples = 0
        gdb.write("Gathering Samples")
        gdb.flush(gdb.STDOUT)
        try:
            for i in range(0, ctx.samples):
                gdb.events.cont.connect(breaking_continue_handler)
                gdb.execute("continue", to_string=True)
                gdb.events.cont.disconnect(breaking_continue_handler)
                for inf in gdb.inferiors():
                    inum = inf.num
                    for th in inf.threads():
                        thn = th.num
                        if thn not in self.threads:
                            f = GDBFunction(None, 2)
                            self.threads[thn] = GDBThread(th.name, thn, th.ptid, f)
                        if ctx.match and not any(m in th.name for m in ctx.match.split(',')):
                             pass
                        elif ctx.exclude and any(m in th.name for m in ctx.exclude.split(',')):  
                             pass
                        else:                           
                            th.switch()
                            frame = gdb.newest_frame()
                            while (frame.older() != None):
                                frame = frame.older()
                            self.threads[thn].function.inverse_add_frame(frame)

                samples += 1
                gdb.write(".")
                gdb.flush(gdb.STDOUT)
        except KeyboardInterrupt:
            pass
        finally:
            print("\nProfiling complete with %d samples." % samples)
            if ctx.output:
                common.dump_threads(self.threads, ctx.output)
            else:
                common.print_callgraph(self.threads)

        if detach_and_kill:
            gdb.execute("detach", to_string=True)
            gdb.execute("quit")
        else:
            pid = gdb.selected_inferior().pid
            os.kill(pid, signal.SIGSTOP)  # Make sure the process does nothing until
                                          # it's reattached.
            gdb.execute("detach", to_string=True)
            gdb.execute("attach %d" % pid, to_string=True)
            os.kill(pid, signal.SIGCONT)
            gdb.execute("continue", to_string=True)

