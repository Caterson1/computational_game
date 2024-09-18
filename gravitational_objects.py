from vectors import *
from physics import *
from combinator import *
from contants import *
G = 6.67e-11

class CelestialBody:
    def __init__(self, pos: Vec = Vec(100000000), velocity: Vec = Vec(), m: float = 0.07346E24, name: str = "the moon", radius: float = 1738.1E3, color: tuple = (255,255,255)):
        self.name = name
        self.n = name
        self.pos = pos
        self.m = m
        self.v = velocity
        self.a = Vec()
        self.forces = []
        self.forcesgrav = []
        self.timer = 0
        self.r = radius
        self.color = color
        self.ychangecounter = 0
        self.orbitstart = None

    def step(self):
        before = math.copysign(1, self.v.y)
        self.pos += self.v * dt
        self.v += self.a * dt
        self. a = force_adder(self.forces, self.forcesgrav) / self.m
        self.timer += dt
        if math.copysign(1, self.v.y) != before:
            self.ychangecounter +=1
            if self.ychangecounter == 1:
                self.orbitstart = self.timer /3600 /24
            if self.ychangecounter == 3:
                self.ychangecounter = 0
                print(f"The period of {self.name.capitalize()} is {(self.timer /3600 /24 - self.orbitstart)} days")
        # print(self.v)

    def __repr__(self):
        return self.name.upper()
        # return f"{self.name.upper()}\n\tPosition: {self.pos}\n\t Velocity: {self.v}\n\t Mass: {self.m} \n\ta: {self.a}"

def force_due_to_gravity(self: CelestialBody, other: CelestialBody):
    r = other.pos - self.pos
    if mag(r) != 0:
        return ((G * self.m * other.m)/((mag(r))**2)) * norm(r)
    return Vec()


class System:
    def __init__(self, list_of_bodies: list = []):
        self.directory = []
        for body in list_of_bodies:
            self.directory.append(body)
        self.combinations = combinator(self.directory)
        print(self.directory)

    def add(self, CelestialBody):
        self.directory.append(CelestialBody)
        self.combinations = combinator(self.directory)

    def update(self):
        self.combinations = combinator(self.directory)

    def gravity_calculations(self):
        for o in self.directory:
            o.forcesgrav = []
        gravitational_forces = []
        # combinations = combinator(self.directory)
        for gravitational_object in self.combinations:
            gravitational_forces.append(force_due_to_gravity(gravitational_object[0], gravitational_object[1]))
        for o in self.directory:
            for z in self.combinations:
                if o in z:
                    if o == z[0]:
                        o.forcesgrav.append(gravitational_forces[self.combinations.index(z)])
                    else:
                        o.forcesgrav.append(-1 * gravitational_forces[self.combinations.index(z)])


    def step(self):
        self.gravity_calculations()
        for o in self.directory:
            o.step()
#
#
#
#
# system = System([CelestialBody(), CelestialBody(Vec(-100000000))])
# system.step()
