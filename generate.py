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
  #ensure the array has sufficient dimension, filling undefined indices with -1
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
  print 'mnu('+str(m)+','+str(n)+','+str(u)+')'

  #???: should we check storage at this point? or should we check within the algorithms themselves?
  if isStored(m, n, u):
    return recall(m, n, u)

  else:
    result = mnu_array(m,n,u)

    store(m,n,u,result)
    return result

#recursive form of the algorithm
def mnu_recursive (m, n, u):
  if isStored(m, n, u):
    return recall(m, n, u)

  #use native operators when possible
  if n == 1:
    #addition
    return m+u-(identity(n))
  #???: can standard multiplication be used when i(1) !== 0?
  elif (n == 2 and (identity(1) == 0)): 
    #multiplication
    return m*(u-identity(2)+1)
  elif (n == 3 and identity(1) == 0 and identity(2) == 1):
    #exponentiation
    return u**(m-identity(3)+1)

  #solve using definition
  elif m == identity(n):
    #print "identity"
    # if m is the identity of n, return u
    return u

  elif n == 1:
    #print "addition"
    # addition.
    return u+m

  else:
    #print "recurse"
    return mnu_recursive(mnu_recursive(m-1, n, u), n-1, u)

  #print 'store('+str(m)+','+str(n)+','+str(u)+','+str(result)+')'

#algorithm converts operation to array rather than making function calls
def mnu_array (m, n, u):
  return mnu_array_helper([u, m], [n])

def mnu_array_helper (um, n):
  #we choose the tail of the array represent the first in order of operations because it's faster to add or remove

  #to make the loop more uniform, we put u at the beginning of the m array

  #while there are more operations to perform...
  #if (um == [3,3] and n[0] == 3):
  #  pdb.set_trace()
  while(len(n) >= 1):
    #p = str(um[0])
    #for i in range(0, len(n)):
    #  p = str(um[i+1]) + "(" + str(n[i]) + ")" +p
    #print p

    topM = um[-1]
    topN = n[-1]
    topU = um[-2]

    #use native operators where possible
    if (topN == 2 and identity(1) == 0):
      um[-2] = topM*(topU-identity(topN)+1)
      n.pop()
      um.pop()

    elif (topN == 3 and identity(1) == 0 and identity(2) == 1):
      um[-2] = topU**(topM-identity(topN)+1)
      n.pop()
      um.pop()

    #solve using definition
    elif identity(topN) == topM:
      #print "identity"
      # if m is the identity of n, return u
      um.pop();
      n.pop();

    elif topN == 1:
      #print "addition"
      # addition.
      um[-2] += topM-(identity(topN))
      um.pop()
      n.pop()

    else:
      #print "recurse"

      um.pop()
      um.pop()
      n.pop()
      #remember to reverse because we evaluate tail first
      um.extend([topU, topU, topM-1])
      n.extend([topN-1, topN])

  return um[0]


with open('public/standard.array.csv', 'w') as csvFile:
  csvWriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
  #begin by writing column names
  csvWriter.writerow(['m','n','u','r'])
  #???: should succession (n=0) be included? succession doesn't have an identity, so I am excluding it
  for n in range(1, boundary['n']+1):
    #this algorithm is not designed for values of m below identity, so start the range at identity
    for m in range(identity(n), boundary['m']+1):
      #inputs where u=0 such as 1,3,0 will eventually become 0,3,0. But we have disallowed m=0. So instead of starting at u=0, start at u=identity
      for u in range(identity(n), boundary['u']+1):
        print '---'
        output = [m, n, u, mnu(m, n, u)]
        print "="+str(output[3])
        csvWriter.writerow(output)

  csvFile.close();