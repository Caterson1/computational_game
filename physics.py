from vectors import *

def force_adder(*forces):
    total_force = Vec()
    for force in forces:
        if isinstance(force, Vec):
            total_force += force
        elif isinstance(force, list):
            for f in force:
                total_force += f
        else:
            raise TypeError("force must be type: Vec or List")
    return total_force
