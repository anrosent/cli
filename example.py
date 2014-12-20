#!/usr/bin/env python3
import cli

def f1(a=None, b=3):
    print("%s:%s"%(a,b))

if __name__ == '__main__':

    runner = cli.CLI()
    runner.add_func(f1, 'first', ('a', {'type':int}), ('b', {'nargs': '?'}))

    runner.run()
