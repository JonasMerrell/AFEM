import numpy as np
from Solve import solve

coords = np.array([[0,0,0], [10,5,0], [10,0,0], [20,8,0], [20,0,0],
                   [30,9,0], [30,0,0], [40,8,0], [40,0,0], [50,5,0],
                   [50,0,0],[60,0,0]])

connect = np.array([[1,3], [3,5], [5,7], [7,9], [9,11], [11,12],
                    [1,2], [2,4], [4,6], [6,8], [8,10], [10,12],
                    [2,3], [4,5], [6,7], [8,9], [10,11], [2,5],
                    [4,7], [7,8], [9,10]])-1

youngs_modulus = np.array([1000]*21)
Abot, Atop, Abat, Adia = 2, 10, 3, 1

area = np.array([Abot, Abot, Abot, Abot, Abot, Abot,
     Atop, Atop, Atop, Atop, Atop, Atop,
     Abat, Abat, Abat, Abat, Abat,
     Adia, Adia, Adia, Adia])

num_nodes = coords.shape[0]

X, Y, Z = (0, 1, 2)
ALL_nodes = range(0,num_nodes,1)
ALL_dofs = range(0,3,1)
loads = [[2,Y,-10.],[4,Y,-10.],[6,Y,-16.],[8,Y,-10.],[10,Y,-10.]]
bcs = [[0, ALL_dofs, 0.], [11, Y, 0.], [ALL_nodes, Z, 0]]

u, R = solve(coords, connect, area, youngs_modulus, loads, bcs)

# from element import stiffness
# from global_stiffness import assemble
# from global_force import format_bcs, global_force, apply_bcs
# K = assemble(coords, connect, area, youngs_modulus)

# doftags, dofvals = format_bcs(loads, bcs, coords)

# F = global_force(doftags, dofvals)

# Kbc, Fbc = apply_bcs(K, F, doftags, dofvals)

# u = np.linalg.solve(Kbc, Fbc)

# Ft = K @ u
# R = Ft - F