#!/usr/bin/env python3
import cli

def greet(name=None, age=0):
    print("Hello, %s. You are %s years old." % (name, age))

def hi():
    print("Hi")

if __name__ == '__main__':

    runner = cli.CLI()
    
    # Commands can be specified with multiple names
    aliases = ['greet', 'g']

    # Specify Args for greet function (see argparse.ArgumentParser.add_argument)
    name_arg = ('name', {'type':str})
    age_arg  = ('age', {'type':int, 'nargs': '?'})
    
    # Add function to CLI
    runner.add_func(greet, aliases, name_arg, age_arg)

    # External CLI
    extern = cli.CLI()
    extern.add_func(hi, 'hi')

    # Add extern CLI to runner
    runner.add_cli('other', extern)

    # Loop from stdin (optionally takes any input stream)
    runner.run()
