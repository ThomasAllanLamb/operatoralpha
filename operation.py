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

def r_bounded_assume_monotonic (m, n, u, ttl, indentation = 1):
  print (".   "*(indentation-1))+"r_bounded ("+str(m)+", "+str(n)+", "+str(u)+", "+str(ttl)+")"

  #temporary catch for floats. We currently can't handle them
  if (m%1 != 0):
    print (".   "*indentation)+"caught float"
    lower = r_bounded_assume_monotonic(math.floor(m), n, u, ttl, indentation+1)
    upper = r_bounded_assume_monotonic(math.ceil(m), n, u, ttl, indentation+1)
    return [lower[0], upper[1]]

  #re-implement isStored later
  #if isStored(m, n, u):
  #  return [recall(m, n, u), 0]

  #use native operators when possible
  if n == 1:
    #addition
    return [u+m-(identity(n)), u+m-(identity(n))]
  elif n == 2: 
    #multiplication
    return [u+(m-identity(2))*(u-identity(1)), u+(m-identity(2))*(u-identity(1))]
  #???: can exponentiation with arbitrary identities be rewritten using native operators?
  elif (n == 3 and identity(1) == 0 and identity(2) == 1):
    #exponentiation
    return [u**(m-identity(3)+1), u**(m-identity(3)+1)]


  elif m < identity(n):
    #print "recurse"
    #???: this seems to add time to live by duplicating it. Is that right? Should we be doing that?
    #???: unsure how to pass the results of r_bounded as a single parameter. Choosing to just take the lower bound for simplicity
    #???: I'm pretty sure this is wrong. Can we assume that the lower bound of the r component being sent to m_bounded will result in a lower range than the upper bound of r being sent to m_bounded?
    rComponent = r_bounded_assume_monotonic(m+1, n, u, ttl, indentation+1)
    lowerR = rComponent[0]
    upperR = rComponent[1]
    lowerM = m_bounded_assume_monotonic(n-1, u, lowerR, ttl, indentation+1)
    upperM = m_bounded_assume_monotonic(n-1, u, upperR, ttl, indentation+1)
    #???: this is not the honest way to combine ranges, but we're doing it
    return [lowerM[0], upperM[1]]
  #solve using definition
  elif m == identity(n):
    #print "identity"
    # if m is the identity of n, return u
    return [u, u]
  elif m > identity(n):
    #print "recurse"
    #!!!: we only accept integers, so if m>identity, we can use positive integer algorithm
    return [r(m,n,u), r(m,n,u)]

def m_bounded_assume_monotonic (n, u, target, ttl, indentation = 1):
  print (".   "*(indentation-1))+"m_bounded ("+str(n)+", "+str(u)+", "+str(target)+", "+str(ttl)+")"
  bounds = [None, None]

  #???: should we start guess at 0?
  #we currently modify our guess by 1 each loop, making test = r(r(guess, 1, 0), n, u). It might make more sense to modify it by some faster-growing function like test = r(r(guess,guess,guess), n, u)
  guess = 0;
  #find initial bounds
  print (".   "*indentation)+"target="+str(target)
  while (bounds[0] is None or bounds[1] is None) and ttl >= 1:
    print (".   "*indentation)+"guess="+str(guess)
    test = r_bounded_assume_monotonic(guess, n, u, ttl, indentation+1)
    print (".   "*indentation)+"test="+str(test)
    if (test[1] < target):
      #guessed too low.
      bounds[0] = guess
      guess += 1
    elif (test[0] <= target and test[1] >= target):
      if (test[0] == target and test[1] == target):
        #we guessed it exactly.
        return [guess, guess]
      else:
        #the target is within the bounds of the test. This doesn't tell us anything.
        #???: this will preferentially guess downward when our initial guess is near the correct answer. Is there a better choice?
        if bounds[0] is None:
          guess -= 1
        elif bounds[1] is None:
          guess += 1
    elif (test[0] > target):
      #guessed too high.
      bounds[1] = guess
      guess -= 1

    ttl -= 1

  if (bounds[0] is None or bounds[1] is None):
    #we were unable to find a valid set of bounds.
    return bounds

  else:
    #bounds is now valid.
    while (ttl >= 1):
      #???: guessing the midpoint is probably not optimal
      guess = (bounds[0]+bounds[1])/2
      test = r_bounded_assume_monotonic(guess, n, u, ttl, indentation+1)
      if (test < target):
        bounds[0] = guess
      elif (test == target):
        return [guess, 0]
      elif (test > target):
        bounds[1] = guess

      ttl -= 1

    return bounds

def r_bounded (m, n, u, ttl, indentation = 1):
  print (".   "*(indentation-1))+"r_bounded ("+str(m)+", "+str(n)+", "+str(u)+", "+str(ttl)+")"

  #temporary catch for floats. We currently can't handle them
  if (m%1 != 0):
    print (".   "*indentation)+"caught float"
    lower = r_bounded_assume_monotonic(math.floor(m), n, u, ttl, indentation+1)
    upper = r_bounded_assume_monotonic(math.ceil(m), n, u, ttl, indentation+1)
    return [lower[0], upper[1]]

  #re-implement isStored later
  #if isStored(m, n, u):
  #  return [recall(m, n, u), 0]

  #use native operators when possible
  if n == 1:
    #addition
    return [u+m-(identity(n)), u+m-(identity(n))]
  elif n == 2: 
    #multiplication
    return [u+(m-identity(2))*(u-identity(1)), u+(m-identity(2))*(u-identity(1))]
  #???: can exponentiation with arbitrary identities be rewritten using native operators?
  elif (n == 3 and identity(1) == 0 and identity(2) == 1):
    #exponentiation
    return [u**(m-identity(3)+1), u**(m-identity(3)+1)]


  elif m < identity(n):
    #print "recurse"
    #???: this seems to add time to live by duplicating it. Is that right? Should we be doing that?
    #???: unsure how to pass the results of r_bounded as a single parameter. Choosing to just take the lower bound for simplicity
    #???: I'm pretty sure this is wrong. Can we assume that the lower bound of the r component being sent to m_bounded will result in a lower range than the upper bound of r being sent to m_bounded?
    rComponent = r_bounded(m+1, n, u, ttl, indentation+1)
    lowerR = rComponent[0]
    upperR = rComponent[1]
    lowerM = m_bounded(n-1, u, lowerR, ttl, indentation+1)
    upperM = m_bounded(n-1, u, upperR, ttl, indentation+1)
    #???: this is not the honest way to combine ranges, but we're doing it
    return [lowerM[0], upperM[1]]
  #solve using definition
  elif m == identity(n):
    #print "identity"
    # if m is the identity of n, return u
    return [u, u]
  elif m > identity(n):
    #print "recurse"
    #!!!: we only accept integers, so if m>identity, we can use positive integer algorithm
    return [r(m,n,u), r(m,n,u)]

def m_bounded (n, u, target, ttl, indentation = 1):
  print (".   "*(indentation-1))+"m_bounded ("+str(n)+", "+str(u)+", "+str(target)+", "+str(ttl)+")"
  bounds = [None, None]


  guessIndex = 0;
  while (guessIndex <= ttl-1):
    guess = guessGenerator(guessIndex)
    
    test = r_bounded(guess, n, u, ttl, indentation+1)

    if (test[0][0] <= target)
    #is target a number? a range of numbers? several ranges? r_bounded returns a possibly-empty array of ranges. How would I compare a range or ranges to a range or ranges?
    #assuming target is a number, the result of this guess is clear if test is strictly bigger. But what do I do if target is within one of those ranges? What do I do if it is between two ranges? I was planning to just note crossovers from strictly lower to strictly higher to infer bounds. But what do those other conditions imply? Anything?
    ##