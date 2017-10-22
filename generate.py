#!/usr/bin/python

import sys
import pdb
import os
import csv
import operation

print 'Argument List:', str(sys.argv)

boundary = {'m': int(sys.argv[1]), 'n': int(sys.argv[2]), 'u': int(sys.argv[3])}
outputRelativePath = "data/standard.csv"

#ensure that target directory exists
outputRelativeDirectory = os.path.dirname(outputRelativePath)
print outputRelativeDirectory
if not os.path.exists(outputRelativeDirectory):
    os.makedirs(outputRelativeDirectory)

with open(outputRelativePath, 'w') as csvFile:
  csvWriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
  #begin by writing column names
  csvWriter.writerow(['m','n','u','r'])
  #???: should succession (n=0) be included? succession doesn't have an identity, so I am excluding it
  for n in range(1, boundary['n']+1):
    #this algorithm is not designed for values of m below identity, so start the range at identity
    for m in range(operation.identity(n), boundary['m']+1):
      #inputs where u=0 such as 1,3,0 will eventually become 0,3,0. But we have disallowed m=0. So instead of starting at u=0, start at u=identity
      for u in range(operation.identity(n), boundary['u']+1):
        print '---'
        output = [m, n, u, operation.r(m, n, u)]
        print "="+str(output[3])
        csvWriter.writerow(output)

  csvFile.close();