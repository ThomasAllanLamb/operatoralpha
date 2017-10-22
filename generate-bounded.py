#!/usr/bin/python

import sys
import pdb
import os
import csv
import operation

print 'Argument List:', str(sys.argv)

boundary = {
  'lowerM': int(sys.argv[1]), 
  'upperM': int(sys.argv[1])+int(sys.argv[4]),
  'lowerN': int(sys.argv[2]), 
  'upperN': int(sys.argv[2])+int(sys.argv[5]),
  'lowerU': int(sys.argv[3]),
  'upperU': int(sys.argv[3])+int(sys.argv[6]),
}
ttl = int(sys.argv[7])

outputRelativePath = "data/bounded.csv"
#ensure that target directory exists
outputRelativeDirectory = os.path.dirname(outputRelativePath)
print outputRelativeDirectory
if not os.path.exists(outputRelativeDirectory):
    os.makedirs(outputRelativeDirectory)

with open(outputRelativePath, 'w') as csvFile:
  csvWriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
  #begin by writing column names
  csvWriter.writerow(['m','n','u','r_midpoint', 'r_spread'])
  #???: should succession (n=0) be included? succession doesn't have an identity, so I am excluding it
  for n in range(boundary['lowerN'], boundary['upperN']):
    for m in range(boundary['lowerM'], boundary['upperM']):
      for u in range(boundary['lowerU'], boundary['upperU']):
        print '--- r('+str(m)+', '+str(n)+', '+str(u)+')'
        r = operation.r_bounded(m, n, u, ttl)
        midpoint = r[0]+r[1]/2
        spread = r[1]
        output = [m, n, u, midpoint, spread]
        print "="+str(r)
        csvWriter.writerow(output)

  csvFile.close();