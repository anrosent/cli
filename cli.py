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
        self.aliases = {}
        self.add_func(self.print_help, ['h', 'help'])
        self.add_func(self.quit,       ['q', 'quit'])

    def add_func(self, callback, names, *args):
        """Adds a command to the CLI - specify args as you would to
        argparse.ArgumentParser.add_argument()
        """

        if isinstance(names, list):
            for name in names:
                self.add_func(callback, name, *args)
                self.aliases[name] = names
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

    def exec_cmd(self, cmdstr):
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

    def print_help(self):
        """Prints usage of all registered commands, collapsing aliases
        into one record
        """
        seen_aliases = set()
        print('-'*80)
        for cmd, (fun, parser) in self.cmds.items():
            if cmd != 'help':
                if cmd not in seen_aliases:
                    if cmd in self.aliases:
                        seen_aliases.update(self.aliases[cmd])
                        cmd = '/'.join(self.aliases[cmd])
                    print(cmd)
                    parser.print_usage()
                    print('-'*80)

    def quit(self):
        """Quits the REPL
        """
        print('Quitting.')
        sys.exit(0)

    def run(self, instream=sys.stdin):
        """Runs the CLI, reading from sys.stdin by default
        """
        for line in instream:
            self.exec_cmd(line)
