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

    def print_samples(self, depth, include_sub):
        print(("%s%s - %s" % (' ' * (self.indent * depth), self.get_samples(include_sub), self.name)))
        for function in self.subfunctions:
            function.print_samples(depth+1)

    def print_percent(self, prefix, total, threshold, include_sub):
#        print "%s%0.2f - %s" % (' ' * (self.indent * depth), self.get_percent(total), self.name)
        subfunctions = {}
        for function in self.subfunctions:
            v = function.get_percent(total, include_sub)
            if function.name is None:
#              print(">>>> name = None")
                function.name = "???"
            if v is None:
#              print(">>>>%s" % (function.name))
                v = "???"
            subfunctions[function.name] = v

        i = 0
        #for name, value in sorted(subfunctions.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        for name, value in sorted(list(subfunctions.items()), key= lambda kv: (kv[1], kv[0]), reverse=True):

            new_prefix = ''
            if i + 1 == len(self.subfunctions):
               new_prefix += '  '
            else:
               new_prefix += '| '

            print(("%s%s%0.2f%% %s" % (prefix, "+ ", value, name)))

            # Do not descend below the threshold 
            if value < threshold:
                continue;

            self.get_func(name).print_percent(prefix + new_prefix, total, threshold, include_sub)
            i += 1

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

