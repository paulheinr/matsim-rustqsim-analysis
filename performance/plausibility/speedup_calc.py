import numpy as np

T_A = 12
W = 0
T_E = 9670
L = 1
D = 4
T_H = 27


def T(p, t_a=T_A, w=W, t_e=T_E, l=L, d=D, t_h=T_H):
    return t_a / p + w + t_e / (p ** 0.822) + 2 * (l + d) + t_h


if __name__ == '__main__':
    logspace = np.logspace(0, 7, num=8, base=2)
    print(logspace)
    print(T(logspace))
