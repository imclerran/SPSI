#!/usr/bin/env python3

import unittest
from HW5 import *

class HW5SampleTests(unittest.TestCase):
    def setUp(self):
        clearBoth()  #clear both stacks
        dictstack.append((0,{}))


    def test_input1Static(self):
        testinput1 = """
             /x 4 def
             /g { x stack } def
             /f { /x 7 def g } def
             f
        """
        opstackOutput = [4]
        dictstackOutput = [(0, {'/x': 4, '/g': ['x', 'stack'], '/f': ['/x', 7, 'def', 'g']})]
        interpreter(testinput1,"static")
        self.assertEqual(opstack,opstackOutput)
        self.assertEqual(dictstack,dictstackOutput)

    def test_input1Dynamic(self):
        testinput1 = """
             /x 4 def
             /g { x stack } def
             /f { /x 7 def g } def
             f
        """
        opstackOutput = [7]
        dictstackOutput = [(0, {'/x': 4, '/g': ['x', 'stack'], '/f': ['/x', 7, 'def', 'g']})]
        interpreter(testinput1,"dynamic")
        self.assertEqual(opstack,opstackOutput)
        self.assertEqual(dictstack,dictstackOutput)

    def test_input2Static(self):
        testinput2 = """
            /m 50 def
            /n 100 def
            /egg1 {/m 25 def n} def
            /chic
    	    {/n 1 def
	           /egg2 { n stack} def
	            m  n
   	           egg1
	           egg2
	        } def
            n
            chic
        """
        opstackOutput = [100, 50, 1, 100, 1]
        dictstackOutput = [(0, {'/m': 50, '/n': 100, '/egg1': ['/m', 25, 'def', 'n'], '/chic': ['/n', 1, 'def', '/egg2', ['n', 'stack'], 'def', 'm', 'n', 'egg1', 'egg2']})]
        interpreter(testinput2,"static")
        self.assertEqual(opstack,opstackOutput)
        self.assertEqual(dictstack,dictstackOutput)

    def test_input2Dynamic(self):
        testinput2 = """
            /m 50 def
            /n 100 def
            /egg1 {/m 25 def n} def
            /chic
    	    {/n 1 def
	           /egg2 { n stack} def
	            m  n
   	           egg1
	           egg2
	        } def
            n
            chic
        """
        opstackOutput = [100, 50, 1, 1, 1]
        dictstackOutput = [(0, {'/m': 50, '/n': 100, '/egg1': ['/m', 25, 'def', 'n'], '/chic': ['/n', 1, 'def', '/egg2', ['n', 'stack'], 'def', 'm', 'n', 'egg1', 'egg2']})]
        interpreter(testinput2,"dynamic")
        self.assertEqual(opstack,opstackOutput)
        self.assertEqual(dictstack,dictstackOutput)

    def test_input3Static(self):
        testinput3 = """
           /x 10 def
           /A { x } def
           /C { /x 40 def A stack } def
           /B { /x 30 def /A { x } def C } def
           B
        """
        opstackOutput = [10]
        dictstackOutput = [(0, {'/x': 10, '/A': ['x'], '/C': ['/x', 40, 'def', 'A', 'stack'], '/B': ['/x', 30, 'def', '/A', ['x'], 'def', 'C']})]
        interpreter(testinput3,"static")
        self.assertEqual(opstack,opstackOutput)
        self.assertEqual(dictstack,dictstackOutput)

    def test_input3Dynamic(self):
        testinput3 = """
           /x 10 def
           /A { x } def
           /C { /x 40 def A stack } def
           /B { /x 30 def /A { x } def C } def
           B
        """
        opstackOutput = [40]
        dictstackOutput = [(0, {'/x': 10, '/A': ['x'], '/C': ['/x', 40, 'def', 'A', 'stack'], '/B': ['/x', 30, 'def', '/A', ['x'], 'def', 'C']})]
        interpreter(testinput3,"dynamic")
        self.assertEqual(opstack,opstackOutput)
        self.assertEqual(dictstack,dictstackOutput)

    def test_input4Static(self):
        testinput4 = """
            /out true def
            /xand { true eq {pop false} {true eq { false } { true } ifelse} ifelse dup /x exch def stack} def
            /myput { out dup /x exch def xand } def
            /f { /out false def myput } def
            false f
        """
        opstackOutput = [False]
        dictstackOutput = [(0, {'/out': True, '/xand': [True, 'eq', ['pop', False], [True, 'eq', [False], [True], 'ifelse'], 'ifelse', 'dup', '/x', 'exch', 'def', 'stack'], '/myput': ['out', 'dup', '/x', 'exch', 'def', 'xand'], '/f': ['/out', False, 'def', 'myput']})]
        interpreter(testinput4,"static")
        self.assertEqual(opstack,opstackOutput)
        self.assertEqual(dictstack,dictstackOutput)

    def test_input4Dynamic(self):
        testinput4 = """
            /out true def
            /xand { true eq {pop false} {true eq { false } { true } ifelse} ifelse dup /x exch def stack} def
            /myput { out dup /x exch def xand } def
            /f { /out false def myput } def
            false f
        """
        opstackOutput = [True]
        dictstackOutput = [(0, {'/out': True, '/xand': [True, 'eq', ['pop', False], [True, 'eq', [False], [True], 'ifelse'], 'ifelse', 'dup', '/x', 'exch', 'def', 'stack'], '/myput': ['out', 'dup', '/x', 'exch', 'def', 'xand'], '/f': ['/out', False, 'def', 'myput']})]
        interpreter(testinput4,"dynamic")
        self.assertEqual(opstack,opstackOutput)
        self.assertEqual(dictstack,dictstackOutput)

    def test_input5Static(self):
        testinput5 = """
            /x [1 2 3 4] def
            /A { x length } def
            /C { /x [10 20 30 40 50 60] def A stack } def
            /B { /x [6 7 8 9] def /A { x 0 get} def C } def
            B
        """
        opstackOutput = [4]
        dictstackOutput = [(0, {'/x': (4, [1, 2, 3, 4]), '/A': ['x', 'length'], '/C': ['/x', (6, [10, 20, 30, 40, 50, 60]), 'def', 'A', 'stack'], '/B': ['/x', (4, [6, 7, 8, 9]), 'def', '/A', ['x', 0, 'get'], 'def', 'C']})]
        interpreter(testinput5,"static")
        self.assertEqual(opstack,opstackOutput)
        self.assertEqual(dictstack,dictstackOutput)

    def test_input5Dynamic(self):
        testinput5 = """
            /x [1 2 3 4] def
            /A { x length } def
            /C { /x [10 20 30 40 50 60] def A stack } def
            /B { /x [6 7 8 9] def /A { x 0 get} def C } def
            B
        """
        opstackOutput = [10]
        dictstackOutput = [(0, {'/x': (4, [1, 2, 3, 4]), '/A': ['x', 'length'], '/C': ['/x', (6, [10, 20, 30, 40, 50, 60]), 'def', 'A', 'stack'], '/B': ['/x', (4, [6, 7, 8, 9]), 'def', '/A', ['x', 0, 'get'], 'def', 'C']})]
        interpreter(testinput5,"dynamic")
        self.assertEqual(opstack,opstackOutput)
        self.assertEqual(dictstack,dictstackOutput)

if __name__ == '__main__':
    unittest.main()

