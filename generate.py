#!/usr/bin/python

import sys
import pdb

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

computed = [[[]]]

def store (m, n, u, r):
  #ensure the array has sufficient dimension
  
  while (len(computed) <= m):
    computed.append([[]])
  while (len(computed[m]) <= n):
    computed[m].append([])
  while (len(computed[m][n]) <= u):
    computed[m][n].append(-1)

  #we have now filled the missing addresses up to and including the target address
  computed[m][n][u] = r

def isStored (m, n, u):
  #has this value already been calculated?
  if (len(computed) >= m+1):
    if (len(computed[m]) >= n+1):
      if (len(computed[m][n]) >= u+1):
        # point exists in computed
        if (computed[m][n][u] != -1):
          return True
        else:
          return False

  #point did not exist in computed
  return False

def recall (m, n, u):
  return computed[m][n][u]


def mnu (m, n, u):
  if isStored(m, n, u):
    return recall(m, n, u)

  #we don't already have the answer.
  else:
    #solve using definition

    if identity(n) == m:
      ##print "identity"
      # if m is the identity of n, return u
      result = u
      store(m,n,u,result)
      return result

    elif n == 1:
      ##print "addition"
      # addition.
      result = u+m
      store(m,n,u,result)
      return result

    else:
      ##print "recurse"
      result = mnu(mnu(m-1, n, u), n-1, u)
      store(m,n,u,result)
      return result

with open('data/standard.csv', 'w') as csvFile:
  csvWriter = csv.writer(csvFile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
  #???: should succession (n=0) be included? succession doesn't have an identity, so I am excluding it
  for n in range(1, boundary['n']+1):
    #this algorithm is not designed for values of m below identity, so start the range at identity
    for m in range(identity(n), boundary['m']+1):
      #inputs where u=0 such as 1,3,0 will eventually become 0,3,0. But we have disallowed m=0. So instead of starting at u=0, start at u=identity
      for u in range(identity(n), boundary['u']+1):
        print "---"
        output = [m, n, u, mnu(m, n, u)]
        csvWriter.writerow(output)
  csvFile.close();