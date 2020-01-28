# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 15:35:40 2019

@author: glubs
"""
import numpy as np
import matlab.engine
eng = matlab.engine.start_matlab()
#from pyfinite import ffield, genericmatrix

#F = ffield.FField(1) #this GF(2^1) = GF(2)

emptytet = [('a'),
 ('b'),
 ('c'),
 ('d'),
 ('a', 'b'),
 ('a', 'c'),
 ('a', 'd'),
 ('b', 'c'),
 ('b', 'd'),
 ('c', 'd'),
 ('a', 'b', 'c'),
 ('a', 'b', 'd'),
 ('a', 'c', 'd'),
 ('b', 'c', 'd')]

skeletontet = [('a'),
 ('b'),
 ('c'),
 ('d'),
 ('a', 'b'),
 ('a', 'c'),
 ('a', 'd'),
 ('b', 'c'),
 ('b', 'd'),
 ('c', 'd')]

def dimcomplex(simp):
    n = len(simp[0])
    for i in range(1, len(simp)):
        temp = len(simp[i])
        if (temp > n):
            n = temp
    return n

def mapchain(simp):
    l = []
    n = dimcomplex(simp)
    for j in range(1, n+1):
        p = 0
        for i in range(len(simp)):
            temp = len(simp[i])
            if temp == j:
                p = p+1
        l.append(p)
    l.append(0)
    l.insert(0, 0)
    #print ("The chain of maps is", l)
    return l
    
#def adjmatrixworking1(simp):
#    n = dimcomplex(simp)
#    l = mapchain(simp)
#    d_1 = np.zeros((6, 4))
#    for i in range(4, 10):
#        for j in range(0, 4):
#            truth = []
#            for k in range(len(simp[j])):
#                if list(simp[j])[k] in simp[i]:
#                    truth.append(True)
#                else:
#                    truth.append(False)
#            if all(truth) == True:
#                d_1[i-4][j] = 1
#    d_1 = d_1.transpose()
#    return d_1

#def adjmatrixworking2(simp):
#    n = dimcomplex(simp)
#    l = mapchain(simp)
#    d_2 = np.zeros((4, 6))
#    for i in range(10, 14):
#        for j in range(4, 10):
#            truth = []
#            for k in range(len(simp[j])):
#                if list(simp[j])[k] in simp[i]:
#                    truth.append(True)
#                else:
#                    truth.append(False)
#            if all(truth) == True:
#                d_2[i-10][j-4] = 1
#    d_2 = d_2.transpose()
#    return d_2


def adjmatrix(simp, m):
    l = mapchain(simp)
    d = np.zeros((l[m+1], l[m]))
    lsum = 0
    usum = l[m+1]
    for a in range(m+1):
        lsum = lsum + l[a]
        usum = usum + l[a]
    for i in range(lsum, usum):
        for j in range(lsum - l[m], usum - l[m+1]):
            truth = []
            for k in range(len(simp[j])):
                if list(simp[j])[k] in simp[i]:
                    truth.append(True)
                else:
                    truth.append(False)
            if all(truth) == True:
                d[i-lsum][j-(lsum - l[m])] = 1
    d = d.transpose()
    return d

def adjmatrixchain(simp):
    l = mapchain(simp)
    chain = []
    for m in range(1, len(l)-1):
        d = adjmatrix(simp, m)
        chain.append(d)
    return chain

# print("The chain of d_i maps for the empty tetrahedron is:")
# for i in range(len(chain_emptytet)-1):
#     print ("d_", i+1, " =  \n", chain_emptytet[i])
#     print ("\n")
        
# print("The chain of d_i maps for the skeleton tetrahedron is:")
# for i in range(len(chain_skeletontet)-1):
#     print ("d_", i+1, " =  \n", chain_skeletontet[i])
#     print ("\n")

def ranks(simp):
    chain = adjmatrixchain(simp)
    rank = []
    for i in range(len(chain)-1):
        A = matlab.double(chain[i].astype(int).tolist())
        b = int(eng.gfrank(A, 2.0))
        rank.append(b)
    rank.insert(0, 0)
    rank.append(0)
    return rank

def betti(simp):
    ranklist = ranks(simp)
    bettis = []
    #print(ranklist)
    for i in range(len(mapchain(simp))-2):
        b = mapchain(simp)[i+1] - ranklist[i] - ranklist[i+1]
        bettis.append(b)
    return bettis

chain_emptytet = adjmatrixchain(emptytet)
bettis_emptytet = betti(emptytet)

chain_skeletontet = adjmatrixchain(skeletontet)
bettis_skeletontet = betti(skeletontet)


print("The chain of d_i maps for the empty tetrahedron is:")
for i in range(len(chain_emptytet)-1):
    print ("d_", i+1, " =  \n", chain_emptytet[i])
    print ("\n")

print("The betti numbers of the empty tetrahedron are:")
for i in range(len(bettis_emptytet)):
    print ("\u03B2_",i, " = ", bettis_emptytet[i])

# print("The chain of d_i maps for the skeleton tetrahedron is:")
# for i in range(len(chain_skeletontet)-1):
#     print ("d_", i+1, " =  \n", chain_skeletontet[i])
#     print ("\n")

# print(betti(emptytet))
# print(betti(skeletontet))







#print(ranks(chain_emptytet))

# d1 = chain_skeletontet[0].astype(int) (THIS IS WORKING CODE)

# A = matlab.double(d1.tolist())

# betti = int(eng.gfrank(A, 2.0))
# print(betti)







# test1 = chain_emptytet[0]
# test2 = chain_emptytet[1]

# v1 = genericmatrix.GenericMatrix((len(test1), len(test1[0])))
# v2 = genericmatrix.GenericMatrix((len(test2), len(test2[0])))

# for i in range(len(test1)):
#     v1.SetRow(i, test1[i])

# for i in range(len(test2)):
#     v2.SetRow(i, test2[i])

# v_test1 = genericmatrix.GenericMatrix.LowerGaussianElim(v1)
# v_test2 = genericmatrix.GenericMatrix.LowerGaussianElim(v2)




