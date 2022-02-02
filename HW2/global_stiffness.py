import numpy as np
import element


def assemble(coords, connect, area, youngs_modulus):
    """Assemble the global finite element stiffness

    Parameters
    ----------
    coords : ndarray
        Nodal coordinates.  coords[n, i] is the ith coordinate of node n
    connect : ndarray
        Element connectivity.  connect[e, n] is the nth node id for element e
    area : ndarray
        area[e] is the element area of the eth element
    youngs_modulus : float
        youngs_modulus[e] is the element elastic modulus of the eth element

    Returns
    -------
    stiff : ndarray
        Global stiffness matrix stored as a full (nd*n, nd*n) symmetric matrix,
        where nd is the number of degrees of freedom per node and n the total
        number of nodes.

    """
    num_dof_per_node = 3
    num_nodes = coords.shape[0]

    stiff = np.zeros((num_nodes * num_dof_per_node, num_nodes * num_dof_per_node))
    for (eid, econn) in enumerate(connect):
        elem_coords = coords[econn]
        elem_stiff = element.stiffness(eid, elem_coords, area[eid], youngs_modulus[eid])
        dof_map = [
            num_dof_per_node * node_id + dof
            for node_id in econn
            for dof in range(num_dof_per_node)
        ]
        for local_row in range(elem_stiff.shape[0]):
            global_row = dof_map[local_row]
            for local_col in range(local_row, elem_stiff.shape[0]):
                global_col = dof_map[local_col]
                stiff[global_row, global_col] += elem_stiff[local_row, local_col]
                stiff[global_col, global_row] = stiff[global_row, global_col]

    return stiff
