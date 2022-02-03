import numpy as np
from global_stiffness import assemble
from global_force import global_force, apply_bcs, format_bcs

def solve(coords, connect, area, youngs_modulus, loads, bcs):
    K = assemble(coords, connect, area, youngs_modulus)
    F = global_force(*format_bcs(loads, bcs, coords))
    Kbc, Fbc = apply_bcs(K, F, *format_bcs(loads, bcs, coords))
    u = np.linalg.solve(Kbc, Fbc)
    Ft = K @ u
    R = Ft - F

    return u, R