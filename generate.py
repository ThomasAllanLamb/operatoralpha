#!/usr/bin/python

import sys

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

boundary = {'m': int(sys.argv[1]), 'n': int(sys.argv[2]), 'u': int(sys.argv[3])}
import csv

#the identity of a given n
def identity (n):
  if n == 1:
    # addition
    return 0
  elif n >= 2:
    return 1

def mnu (m, n, u):
  # Use native operators when possible.
  if n == 0:
    # succession
    return u+1

  elif n == 1:
    # addition
    return u+m

  elif n == 2:
    # multiplication
    return u*m

  elif n == 3:
    # exponentiation
    return u**m

  #no shortcuts were used.
  else:
    #solve using definition
    # if m is the identity of n, return u
    if identity(n) == m:
      return u
    else:
      return mnu(mnu(m-1, n, u), n-1, u)

#build 
output = mnu(boundary['m'], boundary['n'], boundary['u'])

with open('standard.csv', 'w') as csvFile:
  csvWriter = csv.writer(csvFile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
  for n in range(0, boundary['n']+1):
    for m in range(0, boundary['m']+1):
      for u in range(0, boundary['u']+1):
        output = [m, n, u, mnu(m, n, u)]
        csvWriter.writerow(output)
  csvFile.close();