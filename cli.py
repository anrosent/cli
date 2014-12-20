import sys
import argparse

class CLI(object):

    def __init__(self):
        self.cmds = {} 

    def add_func(self, callback, names, *args):
        if isinstance(names, list):
            for name in names:
                self.add_func(callback, name, *args)
        elif isinstance(names, str):
            parser = argparse.ArgumentParser(prog=names)
            for cmd, spec in args:
                parser.add_argument(cmd, **spec)
            self.cmds[names] = (callback, parser)
        else:
            raise TypeError("Command must be specified by str name or list of names")
    
    def dispatch(self, cmd, args):
        if cmd in self.cmds:
            callback, parser = self.cmds[cmd]
            try:
                p_args = parser.parse_args(args)
            except SystemExit:
                return
            callback(**dict(p_args._get_kwargs()))
        else:
            self.invalid_cmd(command=cmd)


    def exec_cmd(self, cmdstr):
        parts = cmdstr.split()
        if len(parts):
            cmd, *args = parts
            self.dispatch(cmd, args)
        else:
            self.invalid_cmd()

    def invalid_cmd(self, command=''):
        print("Invalid Command: %s" % command)


    def run(self, instream=sys.stdin):
        for line in instream:
            self.exec_cmd(line)
