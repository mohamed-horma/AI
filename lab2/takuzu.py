#! /usr/bin/env python3
# -*- coding: utf-8; mode: python -*-

# ENSICAEN
# École Nationale Supérieure d'Ingénieurs de Caen
# 6 Boulevard Maréchal Juin
# F-14050 Caen Cedex France
#
# Artificial Intelligence 2I1AE1
#

# @file takuzu.py
#
# @author Régis Clouard

import sys
from grid import Grid
import signal

WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

class TimeoutFunctionException( Exception ):
    """Exception to raise on a timeout"""
    pass

class TimeoutFunction:

    def __init__( self, function, timeout ):
        "timeout must be at least 1 second."
        self.timeout = timeout
        self.function = function

    def handle_timeout( self, signum, frame ):
        raise TimeoutFunctionException()

    def __call__( self, *args ):
        if not 'SIGALRM' in dir(signal):
            return self.function(*args)
        old = signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.timeout)
        try:
            result = self.function(*args)
        finally:
            signal.signal(signal.SIGALRM, old)
        signal.alarm(0)
        return result

def run_agents( agent, grid_file, timeout, function = None ):
    """ The real main. """
    if function:
        grid = Grid(grid_file, agent, function)
    else:
        grid = Grid(grid_file, agent)
    print("Initial Takuzu:")
    grid.display()
    timed_function = TimeoutFunction(grid.solve, timeout)
    try:
        result = timed_function()
        if result:
            (is_consistent, error_message) = grid.is_goal_state(result)
            if is_consistent:
                print("Takuzu Solved.")
                grid.display(result)
            else:
                print(FAIL)
                grid.display(result)
                print("/!\ Error: Inconsistent solution.")
                print("    " + error_message)
                print(ENDC)
        else:
            print(FAIL + "/!\ No solution. Takuzu unsolved!" + ENDC)
        print("\nStatictics:")
        print("    - Number of explored states: %3d" % (grid.count))
        print("    - Total computation time   : %3.1fs" % (grid.computation_time))

    except TimeoutFunctionException as ex:
        print("Error #1: time out", ex)

def default( str ):
    return str + ' [Default: %default]'

def read_command( argv ):
    """ Processes the command used to run Takuzu from the command line. """
    from optparse import OptionParser
    usageStr = """
    USAGE:      python takuzu.py <options>
    EXAMPLES:   python takuzu.py --agent DFS --grid takuzu1.txt
                OR  python takuzu.py -s DFS -g takuzu.txt
                    - solve grid takuzu1.txt with the naive agent
    """
    parser = OptionParser(usageStr)
    
    parser.add_option('-a', '--agent', dest = 'agent',
                      help = default('the agent to use'),
                      metavar = 'TYPE', default = 'DFS')
    parser.add_option('-g', '--grid', dest = 'grid',
                      help = 'The grid to solve', default = 'takuzu1.txt')
    parser.add_option('-f', '--function', dest = 'function',
                      help = 'The heuristic to use', default = None)
    parser.add_option('-t', '--timeout', dest = 'timeout',
                      help = default('Maximum search time'), default = 2000)
    
    options, otherjunk = parser.parse_args(argv)

    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
    args = dict()
    
    # Choose a Takuzu agent
    try:
        module = __import__('agents')
        if options.agent in dir(module):
            agent = getattr(module, options.agent)
            args['agent'] = agent()
        else:
            raise Exception('Unknown agent: ' + options.agent)
    except ImportError:
        raise Exception('No file agents.py')
    
    args['timeout'] = int(options.timeout)
    args['grid_file'] = "puzzles/" + options.grid

    # Choose a heuristic
    if options.function!= None:
        try:
            module = __import__('agents')
            if options.function in dir(module):
                args['function'] = getattr(module, options.function)
            else:
                raise Exception('Unknown heuristic: ' + options.function)
        except ImportError:
            raise Exception('No file agents.py')
    return args

if __name__ == '__main__':
    """ The main function called when takuzu.py is run
    from the command line:

    > python takuzu.py

    See the usage string for more details.

    > python takuzu.py --help
    > python takuzu.py -h """
    args = read_command(sys.argv[1:]) # Get game components based on input
    print("\n-------------------------------------------------------")
    for arg in sys.argv:
        print(arg, end= " ")
    print("\n-------------------------------------------------------")
    run_agents(**args)
