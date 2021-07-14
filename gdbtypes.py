#!/usr/bin/env python3
# Copyright (c) 2017 Mark Nelson

class GDBThread:
    def __init__(self, name, num, ptid, function):
        self.name = name
        self.num = num
        self.ptid = ptid
        self.function = function

class GDBFunction:

    def __init__(self, name, indent):
        self.name = name
        self.indent = indent
        self.subfunctions = []

        # count of times we terminated here
        self.count = 0

    def add_count(self):
        self.count += 1

    def get_samples(self, include_sub):
        _count = self.count
        if include_sub:
            for function in self.subfunctions:
                _count += function.get_samples(include_sub)
        return _count

    def get_percent(self, total, include_sub):
        return 100.0 * self.get_samples(include_sub) / total

    def get_name(self):
        return self.name;

    def get_func(self, name):
        for function in self.subfunctions:
            if function.get_name() == name:
                return function
        return None

    def get_or_add_func(self, name):
        function = self.get_func(name);
        if function is not None:
            return function;
        function = GDBFunction(name, self.indent)
        self.subfunctions.append(function)
        return function

    def fprint(self, ctx, line):
        print(line[0:ctx.max_width])

    def print_samples(self, ctx, depth, include_sub):
        self.fprint(("%s%s - %s" % (' ' * (self.indent * depth), self.get_samples(include_sub), self.name)))
        for function in self.subfunctions:
            function.print_samples(ctx, depth+1)

    def print_percent(self, ctx, prefix, total, include_sub):
        subfunctions = {}
        for function in self.subfunctions:
            v = function.get_percent(total, include_sub)
            if function.name is None:
                function.name = "???"
            if v is None:
                v = "???"
            subfunctions[function.name] = v

        depth = 0
        for name, value in sorted(list(subfunctions.items()), key= lambda kv: (kv[1], kv[0]), reverse=True):
            line_prefix = "%s%s%0.2f%% " % (prefix, "+ ", value)
            nl_prefix = "%s%s" % (prefix," " * (len(line_prefix)-len(prefix)))
            line = name
            if (ctx.max_width > 0 and ctx.max_width < len(line_prefix) + len(line)):
                # output line will be longer than the max width
                line_max = ctx.max_width - len(line_prefix);
                if (ctx.truncate):
                    # truncate it
                    self.fprint(ctx, line_prefix + line[0:line_max-3] + "...")
                else:
                    # or writap it
                    self.fprint(ctx, line_prefix + line[0:line_max])
                    line = line[line_max:]

                    while (line_max > 0 and len(line) > line_max):
                        self.fprint(ctx, nl_prefix + line[0:line_max])
                        line = line[line_max:]
                    if (len(line) > 0):
                        self.fprint(ctx, nl_prefix + line)
            else:
                # output line is shorter than the max width, so print it
                self.fprint(ctx, "%s%s" % (line_prefix, line))

            # Do not descend below the threshold 
            if value < ctx.threshold:
                continue;

            new_prefix = ''
            if depth + 1 == len(self.subfunctions):
               new_prefix += ' '
            else:
               new_prefix += '|'

            self.get_func(name).print_percent(ctx, prefix + new_prefix, total, include_sub)
            depth += 1

    def add_frame(self, frame):
        if frame is None:
            self.count += 1
        else:
            function = self.get_or_add_func(frame.name())
            function.add_frame(frame.older())

    def inverse_add_frame(self, frame):
        if frame is None:
            self.count += 1
        else:
            function = self.get_or_add_func(frame.name())
            function.inverse_add_frame(frame.newer())

