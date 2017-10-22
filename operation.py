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
    computed[m][n].append(None)

  #we have now filled the missing addresses up to and including the target address
  computed[m][n][u] = r

def isStored (m, n, u):
  #has this value already been calculated?
  if (len(computed) >= m+1):
    if (len(computed[m]) >= n+1):
      if (len(computed[m][n]) >= u+1):
        # point exists in computed
        if (computed[m][n][u] != None):
          return True
        else:
          return False

  #point did not exist in computed
  return False

def recall (m, n, u):
  return computed[m][n][u]

#since we don't allow the algorithm to be chosen, we choose for the user
def r (m, n, u):
  print 'r('+str(m)+','+str(n)+','+str(u)+')'

  #???: should we check storage at this point? or should we check within the algorithms themselves?
  if isStored(m, n, u):
    return recall(m, n, u)

  else:
    result = r_array(m,n,u)

    store(m,n,u,result)
    return result

#recursive form of the algorithm
def r_recursive (m, n, u):
  if isStored(m, n, u):
    return recall(m, n, u)

  #use native operators when possible
  if n == 1:
    #addition
    return u+m-(identity(n))
  elif n == 2: 
    #multiplication
    return u+(m-identity(2))*(u-identity(1))
  #???: can exponentiation with arbitrary identities be rewritten using native operators?
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
    return r_recursive(r_recursive(m-1, n, u), n-1, u)

  #print 'store('+str(m)+','+str(n)+','+str(u)+','+str(result)+')'

#algorithm loops over an array rather than recursing in order to avoid stack overflow
def r_array (m, n, u):
  return r_array_helper([u, m], [n])

def r_array_helper (um, n):
  #we choose the tail of the array represent the first in order of operations because it's faster to add or remove

  #to make the loop more uniform, we put u at the beginning of the m array

  #while there are more operations to perform...
  while(len(n) >= 1):
    topM = um[-1]
    topN = n[-1]
    topU = um[-2]

    #use native operators where possible
    if topN == 2:
      um[-2] = topU+(topM-identity(2))*(topU-identity(1))
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