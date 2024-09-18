import random
from gravitational_objects import *
import pygame as p
import sys  # most commonly used to turn the interpreter off (shut down your game)
from entities import *
import Sprites


p.font.init()

# Constants - sets the size of the window
window_bounds = WIDTH, HEIGHT, scale = 800, 600, (0.5E7 ** -1) / 10
center_to_corner = sqrt((WIDTH / 2) ** 2 + (HEIGHT / 2) ** 2)
origin = x0, y0 = WIDTH / 2, HEIGHT - HEIGHT / 2  # This is the new origin
timer = 0
font = p.font.SysFont('Monocraft', 20)
bigfont = p.font.SysFont('Monocraft', 80)
null = CelestialBody(Vec())
null.name = "null"
tracking = null
warning_timer = 0
flasher = True


def xy(entity):
    return x0 + entity.pos.x * scale, y0 - entity.pos.y * scale


screen = p.display.set_mode((WIDTH, HEIGHT))


def pygame_init():
    # Screen or whatever you want to call it is your best friend - it's a canvas
    # or surface where you can draw - generally you'll have one large canvas and
    # additional surfaces on top - effectively breaking things up and giving
    # you the ability to have multiples scenes in one window
    p.init()
    screen.fill((180, 210, 255))
    p.display.set_caption('Fireworks')


def drawer(object_list, place_to_draw_stuff=screen):
    for i in object_list:
        # p.draw.circle(place_to_draw_stuff, i.color, xy(i), 10)
        p.draw.circle(place_to_draw_stuff, i.color, xy(i), i.r * scale)


def universe_drawer(uni):
    for i in uni.planets[0].space_ship_list:
        p.draw.circle(screen, (80, 80, 80, 10), xy(i), i.range * scale)
    drawer(uni.planets)
    for i in uni.asteroids:
        if mag(i.pos * scale) < center_to_corner:
            p.draw.circle(screen, i.color, xy(i), i.r * scale)
    for planet in uni.planets:
        for i in planet.space_ship_list:
            p.draw.circle(screen, i.color.tuple(3), xy(i), i.r * scale)


def get_object_at(x):
    global universe
    global warning_timer
    locations = [[i, mag(Vec(i.pos.x * scale - x.x, i.pos.y * scale - x.y))] for i in universe.master_list()]
    locations.sort(key=lambda sorter: sorter[1])
    if mag(x - locations[0][0].pos * scale) <= locations[0][0].r * scale:
        universe.click_manager(locations[0][0], x)
        return locations[0][0]
    else:
        # if universe.money >= pricesheet["turret"]:
        #     universe.add_spaceship(x / scale + Vec(x0, y0))
        #     universe.money -= pricesheet["turret"]
        # else:
        #     warning_timer += 50
        return None

# BACKGROUND CODE --------------------------------------------------------------
backgrounds = [p.image.load("C:\\Users\\Super\\PycharmProjects\\game1\\Sprites\\Space Background (1).png").convert_alpha(),
               p.image.load("C:\\Users\\Super\\PycharmProjects\\game1\\Sprites\\Space Background (2).png").convert_alpha()]
bg = random.choice(backgrounds)
# BACKGROUND CODE --------------------------------------------------------------

clock = p.time.Clock()

# PUT SETUP CODE HERE ----------------------------------------------------------
universe = Universe()
# print([spaceship for planet in universe.planets for spaceship in planet.space_ship_list])
universe.generate_asteroids()
flasherswitch = p.USEREVENT + 1
p.time.set_timer(flasherswitch, 500)
# PUT SETUP CODE HERE ----------------------------------------------------------
running = True
while True:
    mouse = p.mouse.get_pos()
    mouse = Vec(mouse[0] - x0, y0 - mouse[1])
    # keystroke example
    for event in p.event.get():
        if event.type == flasherswitch:
            flasher = not flasher

        if event.type == p.QUIT:  # this refers to clicking on the "x"-close
            p.quit()
            sys.exit()

        elif event.type == p.MOUSEBUTTONDOWN:
            if event.button == 1: # LEFT MOUSE BUTTON
                get_object_at(mouse)
            if event.button == 3: # RIGHT MOUSE BUTTON
                if universe.money >= pricesheet["turret"]:
                    universe.add_spaceship(mouse / scale + Vec(x0, y0))
                    universe.money -= pricesheet["turret"]
                else:
                    warning_timer += 50

        elif event.type == p.KEYUP:
            x = 0

        elif event.type == p.KEYDOWN:  # there's a separate system built in
            if event.key == p.K_SPACE:
                if running is False:
                    running = True
                    print("START")
                elif running is True:
                    running = False
                    print("PAUSE")
            if event.key == p.K_p:
                print(universe.planets[0].space_ship_list)
            if event.key == p.K_UP:
                screen.fill((0, 0, 0))
                mod = p.key.get_mods()
                if mod == p.KMOD_LSHIFT:
                    scale = scale * 10
                elif mod == p.KMOD_RSHIFT:
                    scale = scale * 100
                else:
                    scale = scale * 2

            if event.key == p.K_DOWN:
                screen.fill((0, 0, 0))
                mod = p.key.get_mods()
                if mod == p.KMOD_LSHIFT:
                    scale = scale / 10
                elif mod == p.KMOD_RSHIFT:
                    scale = scale / 100
                else:
                    scale = scale / 2
            if p.K_1 <= event.key <= p.K_9:
                panx = 0
                pany = 0
                print(event.key, p.K_1)
                starter = event.key - p.K_1
                # mod = p.key.get_mods()
                # if mod == p.KMOD_LSHIFT or p.KMOD_RSHIFT:
                #     starter += 9
                # if mod == p.KMOD_LCTRL or p.KMOD_RCTRL:
                #     starter += 18
                try:
                    tracking = universe.planets[starter]
                except IndexError:
                    tracking = universe.planets[0]
                else:
                    tracking = universe.planets[starter]
                print(starter)
            elif event.key == p.K_F12:
                print("DEBUG MODE ON")
                universe.money = 99999999999999999

    x0 = -tracking.pos.x * scale + WIDTH / 2
    y0 = tracking.pos.y * scale + HEIGHT / 2

    if running:
        clock.tick()
        if clock.get_fps() > 0:
            fps_adjust = 144/clock.get_fps()
        else:
            fps_adjust = 1
        # background
        for z in range(1):
            universe.step(fps_adjust)
            screen.blit(bg, (0,0))
            universe_drawer(universe)
            for drawingtext in range(1):
                money = font.render(f'{universe.money} moneys', False, (255, 255, 255), None)
                moneyrect = money.get_rect()
                moneyrect.topleft = (10, 10)
                screen.blit(money, moneyrect)

                turretcost = font.render(f'COST OF TURRET: {pricesheet["turret"]}', False, (255, 255, 255), None)
                tcrect = turretcost.get_rect()
                tcrect.topright = (WIDTH - 10, 10)
                screen.blit(turretcost, tcrect)

                turretcost1 = font.render(f'RIGHT CLICK TO ADD', False, (255, 255, 255), None)
                tcrect1 = turretcost.get_rect()
                tcrect1.topright = (WIDTH - 15, 35)
                screen.blit(turretcost1, tcrect1)

                health = font.render(f'HEALTH: {universe.planets[0].health}', False, (255, 255, 255), None)
                if universe.gameover:
                    health = font.render(f'HEALTH: 0', False, (255, 255, 255), None)
                healthrect = health.get_rect()
                healthrect.bottomleft = (10, HEIGHT - 10)
                screen.blit(health, healthrect)

                roundcounter = font.render(universe.rctxt, False, (255, 255, 255), None)
                roundcountrect = roundcounter.get_rect()
                roundcountrect.center = (WIDTH/2, 4 * HEIGHT/10)
                screen.blit(roundcounter, roundcountrect)

                if warning_timer > 0:
                    warning = font.render("treasury insufficient", False, (255, 67, 50), None)
                    warningrect = warning.get_rect()
                    warningrect.center = (WIDTH / 2, HEIGHT-25)
                    screen.blit(warning, warningrect)
                    warning_timer -= dt * fps_adjust

                if flasher and universe.gameover:
                    GAMEOVER = bigfont.render("GAME OVER", False, (255, 255, 255), None)
                    GAMEOVERRECT = GAMEOVER.get_rect()
                    GAMEOVERRECT.center = (WIDTH / 2, HEIGHT/2)
                    screen.blit(GAMEOVER, GAMEOVERRECT)
                    warning_timer -= dt * fps_adjust

                if flasher and not running:
                    PAUSED = bigfont.render("GAME PAUSED", False, (255, 255, 255), None)
                    PAUSEDRECT = PAUSED.get_rect()
                    PAUSEDRECT.center = (WIDTH / 2, HEIGHT/2)
                    screen.blit(PAUSED, PAUSEDRECT)
                    warning_timer -= dt * fps_adjust
            # screen.fill((0, 0, 0))
    p.display.flip()

    # This sets an upper limit on the frame rate (here 100 frames per second)
    # often you won't be able