# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
number_rocks = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def increment_angle_vel(self, amount):
        self.angle_vel = amount
        
    def decrement_angle_vel(self, amount):
        self.angle_vel = amount
    
    def turn_thrust(self):
        self.thrust = not self.thrust
        if self.thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
        
    def shoot(self): 
        global a_missile

        orientation = angle_to_vector(self.angle)
        vel = [self.vel[0] + orientation[0] * 5, self.vel[1] + 5 * orientation[1]]
        pos = [self.pos[0] + self.image_center[0] * orientation[0], 
               self.pos[1] + self.image_center[1] * orientation[1]]
        a_missile = Sprite(pos, vel, 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)

    def draw(self,canvas):
        pos_center = [int(self.thrust) * self.image_size[0] + self.image_center[0], self.image_center[1]]
        canvas.draw_image(self.image, pos_center, self.image_size, 
                          self.pos, self.image_size, self.angle)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        
        self.vel[0] *= 0.99
        self.vel[1] *= 0.99
        
        oriention = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += oriention[0] / 10
            self.vel[1] += oriention[1] / 10
            
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius

# helper functions fo Sprite class
def process_sprite_group(canvas, group):
    for sprite in list(group):
        if sprite.update():
            group.remove(sprite)
        sprite.draw(canvas)

def group_collide(group, other_object):
    global number_rocks
    for element in list(group):
        if element.collide(other_object):
            group.remove(element)
            number_rocks -= 1
            return True
    return False

def group_group_collide(group1, group2):
    number_colide = 0
    for element in list(group1):
        if group_collide(group2, element):
            group1.remove(element)
            number_colide += 1
    return number_colide
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]    
        self.pos[1] += self.vel[1]
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        self.age += 1
        
        if self.age >= self.lifespan:
            return True
        return False
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self, other_object):
        if dist(self.get_position(), other_object.get_position()) <= self.get_radius() + other_object.get_radius():
            return True
        return False
           
def draw(canvas):
    global time, lives, score, started, rock_group, missile_group, my_ship, number_rocks
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    
    # update ship and sprites
    my_ship.update()
    if group_collide(rock_group, my_ship):
        lives -= 1
    score += group_group_collide(missile_group, rock_group)
    
    # life and score hub
    canvas.draw_text("life = " + str(lives), (10, 30), 24, "White")
    canvas.draw_text("score = " + str(score), (WIDTH - 120, 30), 24, "White")
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    
    # game update
    if lives <= 0:
        started = False
        rock_group = set([])
        missile_group = set([])
        lives, score = 3, 0
        number_rocks = 0
        timer.stop()
        soundtrack.pause()
            
# timer handler that spawns a rock    
def rock_spawner():
    global number_rocks

    if number_rocks < 12:
        vel = [random.randrange(-1, 1), random.randrange(-1, 1)]
        pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        while dist(pos, my_ship.get_position()) < 4 * my_ship.get_radius():
            pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        angle_vel = (random.randrange(-9, -1) + random.randrange(1, 10)) / 100.0
        a_rock = Sprite(pos, vel, 1, angle_vel, asteroid_image, asteroid_info)
        rock_group.add(a_rock)
        number_rocks += 1

def keydown_handler(key):
    global my_ship
    if key == simplegui.KEY_MAP["left"]:
        my_ship.increment_angle_vel(-0.05)
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.increment_angle_vel(0.05)
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.turn_thrust()
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
        
def keyup_handler(key):
    global my_ship
    if key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["right"]:
        my_ship.decrement_angle_vel(0)
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.turn_thrust()

def mouse_handler(pos):
    global started
    if not started:
        started = True
        timer.start()
        soundtrack.rewind()
        soundtrack.play()

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
frame.set_mouseclick_handler(mouse_handler)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
#timer.start()
frame.start()
