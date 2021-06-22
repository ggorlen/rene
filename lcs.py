######## rene boilerplate ########
import numpy as np

def array_of_zeros(*dimensions, dtype=np.int32):
    return np.zeros([x + 1 for x in dimensions], dtype)
table_of_zeros = array_of_zeros

def array_from_iterable(it):
    arr = np.array(tuple(it))
    padded = np.zeros([1 + x for x in arr.shape], dtype=arr.dtype)
    padded[tuple([slice(1, None) for _ in arr.shape])] = arr
    return padded

INFINITY = float("inf")
NEGATIVE_INFINITY = -INFINITY
######## end rene boilerplate ########

def lcs(n, m, x, y):
    x = array_from_iterable(x)
    y = array_from_iterable(y)
    T = array_of_zeros(n, m)
    
    for i in range(0, (n) + 1):
        T[i][0] = 0
    
    for j in range(0, (m) + 1):
        T[0][j] = 0
    
    for i in range(1, (n) + 1):
        for j in range(1, (m) + 1):
            if x[i] == y[j]:
                T[i][j] = T[i - 1][j - 1] + 1
            else:
                T[i][j] = max(T[i - 1][j], T[i][j - 1])
    
    return T[n][m]
