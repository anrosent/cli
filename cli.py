"""Simple CLI-builder

Build interactive Command Line Interfaces, leaving the argument
validation and parsing logic to the `argparse` Standard Library module.
"""
import sys
import argparse


class CLI(object):
    """The Command Line Interface runner        
    """

    def __init__(self):
        self.cmds = {} 

    def add_func(self, callback, names, *args):
        """Adds a command to the CLI - specify args as you would to
        argparse.ArgumentParser.add_argument()
        """

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
    
    def _dispatch(self, cmd, args):
        """Attempt to run the given command with the given arguments
        """
        if cmd in self.cmds:
            callback, parser = self.cmds[cmd]
            try:
                p_args = parser.parse_args(args)
            except SystemExit:
                return
            callback(**dict(p_args._get_kwargs()))
        else:
            self._invalid_cmd(command=cmd)

    def _exec_cmd(self, cmdstr):
        """Parse line from CLI read loop and execute provided command
        """
        parts = cmdstr.split()
        if len(parts):
            cmd, *args = parts
            self._dispatch(cmd, args)
        else:
            pass

    def _invalid_cmd(self, command=''):
        print("Invalid Command: %s" % command)


    def run(self, instream=sys.stdin):
        """Runs the CLI, reading from sys.stdin by default
        """
        for line in instream:
            self._exec_cmd(line)
