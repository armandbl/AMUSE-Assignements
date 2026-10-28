# live coding session

from amuse.lab import *
from amuse.ext.orbital_elements import get_orbital_elements_from_binary, new_binary_from_orbital_elements
from matplotlib import pyplot as plt
from amuse.plot import scatter
from amuse.community.ph4.interface import ph4

def intitial_conditions():
    
    msun = 1.0 | units.MSun    
    msaturn = 0.0002857 | units.MSun
    a_saturn = 9.5826 | units.AU
    e_saturn = 0.0565
    
    binary = new_binary_from_orbital_elements(msun, msaturn, a_saturn, e_saturn)
    binary[0].name = "Sun"
    binary[1].name = "Saturn"
    print(binary)
    
    a_japetus = 3.5617e6 |units.km
    e_japetus = 0.028
    m_japetus = 1.8e21 | units.kg
    
    japetus_binary = new_binary_from_orbital_elements(msaturn, m_japetus, a_japetus, e_japetus)
    japetus_binary[0].name = "Fake_Saturn"
    japetus_binary[1].name = "Japetus"
    print(japetus_binary)
    
    # center the binary system on the primary body (Saturn)
    japetus_binary.position -= japetus_binary[0].position
    japetus_binary.velocity -= japetus_binary[0].velocity
    print(japetus_binary)
    japetus_binary.position += binary[1].position
    japetus_binary.velocity += binary[1].velocity
    
    japetus = japetus_binary[1]
    binary.add_particle(japetus)
    
    return binary

if __name__ == '__main__':
    bodies = intitial_conditions()
    print(bodies)
    plt.figure(figsize=(8, 8))
    scatter(bodies.position.x, bodies.position.y,c = 'b')
    # plt.show()
    
    a = [] |units.AU
    e = []
    for pair in [bodies[0:2], bodies[1:3]]:
        mass1, mass2, semi_major_axis, eccentricity, *_ = get_orbital_elements_from_binary(pair, G=constants.G)
        a.append(semi_major_axis)
        e.append(eccentricity)

    print("Semi-major axes:", a)
    print("Eccentricities:", e)
    
    converter = nbody_system.nbody_to_si(bodies.mass.sum(), 1 |units.au)
    gravity = ph4(converter)
    gravity.particles.add_particles(bodies)
    channel_from_gravity = gravity.particles.new_channel_to(bodies)
    
    
    gravity.evolve_model(2 | units.yr)
    channel_from_gravity.copy()
    scatter(bodies.position.x, bodies.position.y,c = 'r')
    plt.show()