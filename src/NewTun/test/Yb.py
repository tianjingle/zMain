#  线性方程组
import numpy as np
from scipy import linalg

# 定义A矩阵
A = np.array([[1, 2, 3],
              [1, 3, 5],
              ])

A1 = np.array([[1, 2],
              [1, 3],
              ])
# 定义b
b = np.array([4, 6])

x = linalg.solve(A1, b)
#特解
print(x)

#通解
b_1 = np.array([-3,-5])
x_1 = linalg.solve(A1,b_1)
print(x_1)