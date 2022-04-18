import numpy as np

# m代表系数矩阵。
from scipy.linalg import solve

m = np.array([[1, -2, 1],
              [0, 2, -8],
              [-4, 5, 9]])

m = np.array([[2.772, 16.5225, 4.816,8.332,1.8133333],
              [17120, 13400, 33140,30020,40300],
              [660, 750,2080,1520,2133.333],
              [1, 1,1,1,1]])

# v代表常数列
v = np.array([3.04, 23183.333, 1700,1])
v = np.array([3.04, 23183.333, 1700])

k=np.linalg.matrix_rank(m)#返回矩阵的秩
print(k)
print(np.linalg.det(m))
#返回矩阵的行列式)
# 解线性代数。
r = solve(m, v)

print("结果：")
name = ["X1", "X2", "X3", "X4", "X5"]
for i in range(len(name)):
    print(name[i] + "=" + str(r[i]))
