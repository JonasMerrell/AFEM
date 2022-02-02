import numpy as np
from global_stiffness import assemble
from global_force import global_force, assemble_force, format_bcs

def solve(coords, connect, area, youngs_modulus, loads, bcs):
    K = assemble(coords, connect, area, youngs_modulus)
    Kbc, Fbc = assemble_force(K, coords, loads, bcs)
    F = global_force(*format_bcs(loads, bcs, coords))
    u = np.linalg.solve(Kbc, Fbc)
    Ft = K @ u
    R = Ft - F

    return u, R