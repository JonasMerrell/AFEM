import numpy as np

def format_bcs(loads, bcs, coords):
    num_nodes = coords.shape[0]
    dof_per_node = coords.shape[1]
 
    doftags = np.zeros([num_nodes, dof_per_node])
    dofvals = np.zeros([num_nodes, dof_per_node])
    for bc in bcs:
        doftags[bc[0],bc[1]] = 1
        dofvals[bc[0],bc[1]] = bc[2]
    for load in loads:
        dofvals[load[0],load[1]] = load[2]
    return doftags, dofvals

def global_force(doftags, dofvals):
    F = []
    for i in range(doftags.shape[0]):
        for j in range(doftags.shape[1]):
            if doftags[i,j] == 0:
                F.append(dofvals[i,j])
            else:
                F.append(0)
    
    return np.array(F)

def apply_bcs(K, F, doftags, dofvals):
    
    Kbc = K.copy()
    Fbc = F.copy()
    num_nodes = doftags.shape[0]
    dof_per_node = doftags.shape[1]
    
    for node in range(num_nodes):
        for element_dof in range(dof_per_node):
            if doftags[node, element_dof] == 1:
                global_dof = dof_per_node * node + element_dof
                
                # apply bcs to K
                # K_ij = K_ji = kronecker_ij
                Kbc[global_dof, :] = 0
                Kbc[:, global_dof] = 0
                Kbc[global_dof, global_dof] = 1
                
                # apply bcs to F
                # F_j = { u_i if i =j, F_j - K_jiu_i if i != j
                u = dofvals[node, element_dof]
                Fbc -= np.array([K[j, global_dof] * u for j in range(num_nodes * dof_per_node)])
                Fbc[global_dof] = u
    
    return Kbc, Fbc

def assemble_force(K, coords, loads, bcs):
    doftags, dofvals = format_bcs(loads, bcs, coords)
    F = global_force(doftags, dofvals)
    Kbc, Fbc = apply_bcs(K, F, doftags, dofvals)
    return Kbc, Fbc
            
                
                
                
                