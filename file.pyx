import numpy as np
cimport numpy as np
cimport cython
from cython.parallel import prange, parallel


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)

cpdef condition_2(a, N, m, f, epsilon, w, rho, h, pos, neg):
        cdef:
            int i,j,iter, k
            double x
            np.ndarray b, r
		
        
        for k in range(m):
            b=np.copy(a)
            r=np.zeros((N,N))
            for (i,j), x in np.ndenumerate(a):
                if i == 0 or i == N-1 or j == 0 or j == N-1:
                    continue
                else:
                    r[i,j] = (a[i-1,j]+a[i+1,j]+a[i,j-1]+a[i,j+1])/4 - a[i,j]+np.pi*(h**2)*rho*(pos[i,j]-neg[i,j])
                    a[i,j] = a[i,j] + w*r[i,j]
            
            if k//4 == k/4 and f(a, b)<epsilon:
                print(a,b)

                iter=k
                break



                
        
        return a, iter
    
