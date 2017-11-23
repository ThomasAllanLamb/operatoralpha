#!/usr/bin/python

import sys
import pdb
import os
import operation

print 'Argument List:', str(sys.argv)

r_bounds = operation.r_bounded_assume_monotonic(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))

print "min\tmax"
print str(r_bounds[0])+"\t"+str(r_bounds[1])