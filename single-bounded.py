#!/usr/bin/python

import sys
import pdb
import os
import operation

print 'Argument List:', str(sys.argv)

print operation.r_bounded(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))