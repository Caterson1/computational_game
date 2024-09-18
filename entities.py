from vectors import *
from contants import *
from physics import *
from sympy import *
from level_sheet import level_sheet

type_dict = {"planet": 0, "asteroid": 1, "turret": 1, "mine": 2}
pricesheet = {"planet": 10000, "turret": 1000, "mine": 500}
asteroid_colors = [(0, 0, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (255, 125, 125), (255, 0, 255)]


class Planet:
    def __init__(self, position: Vec = Vec()):
        self.pos = position
        self.m = 1.989e+31 * 2
        self.v = Vec()
        self.a = Vec()
        self.r = 6.9634E8
        self.type = 0
        self.health = 50000
        self.space_ship_list = []
        self.color = (255, 255, 255)

    def step(self):
        self.pos = self.pos

    def death(self):
        for ship in self.space_ship_list:
            ship.death()
            del ship

    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.death()
            return True

    def heal(self, amount: int):
        self.health += amount
        
    def add_spaceship(self, pos: Vec, type: int = 0):
        self.space_ship_list.append(Turret(self, pos))

    def click(self):
        return

    def __repr__(self):
        # return f"\nPlanet: \n\tHealth: {self.health} \n\tSpaceships: {self.space_ship_list} \n\tPosition: {self.pos}"
        return "Planet"


class Turret:
    def __init__(self, planet: Planet, pos: Vec):
        "body dictates the body that will be orbited, and distance is the distance from that body in meters"
        self.relpos = pos - planet.pos
        self.distance = mag(self.relpos)
        self.planet = planet
        self.pos = pos
        self.v = math.sqrt((G * planet.m)/self.distance) * norm(pos.cross(Vec(0,0,1)))
        self.speed = 1
        self.color = Vec(38, 132, 186)
        self.colormax = Vec(38, 132, 186)
        self.r = 6.9634E8
        self.m = 100
        self.force_mag = (G * self.m * planet.m)/(self.distance**2)
        self.a = self.force_mag * norm(self.planet.pos - self.pos) / self.m
        self.level = 1
        self.cooldownmax = 2000 - self.level
        self.cooldown = 2000
        self.range = self.r * (10 + self.level * 1)
        self.SHOW_RANGE = True

    def click(self):
        a = 10
        # self.level += 1
        # self.cooldownmax -= 1
        # self.range = self.r * (20 + self.level)
        # if self.level == 2:
        #     self.colormax = Vec(255, 0, 0)
        # elif self.level == 3:
        #     self.colormax = Vec(255, 255, 0)
        # elif self.level == 4:
        #     self.colormax = Vec(0, 255, 0)
        # elif self.level == 5:
        #     self.colormax = Vec(0, 255, 255)

    def step(self, fps_adjust):
        self.pos += self.v * dt * fps_adjust
        self.pos = norm(self.pos) * self.distance
        self.v = math.sqrt((G * self.planet.m)/mag(self.pos - self.planet.pos)) * norm(self.pos.cross(Vec(0,0,1))) * 100
        self.a = self.force_mag*norm(self.planet.pos-self.pos)/self.m
        self.cooldown += dt
        if self.color != self.colormax:
            self.color += (self.colormax / 2000)
            if self.color.x > self.colormax.x:
                self.color.x = self.colormax.x
            if self.color.y > self.colormax.y:
                self.color.y = self.colormax.y
            if self.color.z > self.colormax.z:
                self.color.z = self.colormax.z

    def death(self):
        del self

    def __repr__(self):
        return f"TURRET LEVEL: {self.level}; {self.distance}m away from a planet"


class Asteroid():
    def __init__(self, position: Vec, level: int = 1):
        self.pos = position
        self.v = Vec()
        self.a = Vec()
        self.gravforces = []
        self.m = 9.1E20
        self.r = 1E9
        self.level = level
        self.color = asteroid_colors[level]
        if self.level > 3:
            self.m *= 10

    def grav(self, gravitational_objects: list):
        self.gravforces = []
        for i in gravitational_objects:
            r = i.pos - self.pos
            self.gravforces.append(((G * self.m * i.m) / ((mag(r)) ** 2)) * norm(r))

    def step(self, planets, fps_adjust):
        self.grav(planets)
        self.pos += self.v * dt * fps_adjust
        self.v += self.a * dt * 20000 * fps_adjust
        self.a = force_adder(self.gravforces) / self.m
        if self.a == 0:
            print(f"ASTEROID {self} not moving")

    def click(self):
        return self.damage()

    def damage(self):
        self.level -= .5
        self.color = asteroid_colors[int(self.level + 1)]
        if self.level < 1:
            return True
        else:
            return False

    def __repr__(self):
        return f"Level {self.level} Asteroid at {self.pos}"


class Universe:
    def __init__(self):
        self.gameover = False
        self.planets = [Planet()]
        self.asteroids = []
        self.selecteddict = ["turret"]
        self.selected = 0
        self.level = 1
        self.money = 0
        self.range = 5E10
        self.rctxttimer = 0
        self.rctxt = None
        self.moneyperkill = 100

    def master_list(self):
        return self.planets + self.asteroids + [spaceship for planet in self.planets for spaceship in planet.space_ship_list]

    def add_spaceship(self, location, type: int = 1):
        "adds a spaceship to a planet: turret = 1, mine = 1"
        if not self.gameover:
            planets = sorted([[spaceship, mag((spaceship.pos - location))] for spaceship in self.planets], key=lambda plan: plan[1])
            planet = planets[0][0]
            # if self.money >= pricesheet[type] and type > 0:
            #     planet.add_spaceship(type)
            #     self.level += pricesheet[type]/100
            planet.add_spaceship(location)

    def add_planet(self, mousexy: tuple):
        self.planets.append(Planet(mousexy[0], mousexy[1]))

    def generate_asteroids(self):
        if self.level <= len(level_sheet) - 1:
            for x in level_sheet[self.level]:
                pos = randvec() * self.range
                pos.z = 0
                self.asteroids.append(Asteroid(pos, x))
        else:
            for x in range(fibonacci(self.level - 4)):
                pos = randvec()*self.range
                pos.z = 0
                self.asteroids.append(Asteroid(pos, random.randrange(1, 6)))

    def asteroid_step(self):
        for a in self.asteroids:
            a.step(self.planets)

    def step(self, fps_adjust):
        if not self.gameover:
            self.physics(fps_adjust)
            self.check_collisions()
            if not self.asteroids:
                self.level += 1
                self.planets[0].heal(3)
                self.generate_asteroids()
                self.rctxttimer = 1000
                self.rctxt = f"Round {self.level}"
                self.money += 500
            if self.rctxttimer == 0:
                self.rctxt = None
            else:
                self.rctxttimer -= 1


    def check_collisions(self):
        for asteroid in self.asteroids:
            if mag(asteroid.pos) < (self.planets[0].r + asteroid.r):
                if self.planets[0].damage(asteroid.level):
                    self.gameover = True
                self.asteroids.remove(asteroid)
                del asteroid
                self.money += self.moneyperkill
        for asteroid in self.asteroids:
            for turret in self.planets[0].space_ship_list:
                if turret.cooldown >= turret.cooldownmax:
                    if mag(turret.pos - asteroid.pos) < (turret.range + asteroid.r):
                        asteroid.click
                        if asteroid.click():
                            try:
                                self.asteroids.remove(asteroid)
                            except:
                                pass
                            self.money += self.moneyperkill
                        turret.cooldown = 0
                        turret.color = turret.color / 2

    def physics(self, fps_adjust):
        for asteroid in self.asteroids:
            if asteroid.level < 1:
                self.asteroids.remove(asteroid)
            asteroid.step(self.planets, fps_adjust)
        for planet in self.planets:
            for spaceship in planet.space_ship_list:
                spaceship.step(fps_adjust)

    def click_manager(self, to_be_clicked, pos):
        if not self.gameover:
            if to_be_clicked.click() == "delete":
                if to_be_clicked in self.planets:
                    self.planets.remove(to_be_clicked)
                elif to_be_clicked in self.asteroids:
                    if to_be_clicked.click():
                        self.asteroids.remove(to_be_clicked)
                        self.money += self.moneyperkill
                else:
                    to_be_clicked.planet.space_ship_list.remove(to_be_clicked)
                del to_be_clicked
