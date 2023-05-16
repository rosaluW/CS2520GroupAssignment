import numpy as np
import pygame as pg
from random import randint, gauss

pg.init()
pg.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

SCREEN_SIZE = (800, 491)
#background image
background = pg.image.load('background.jpeg')


def rand_color():
    return (randint(0, 255), randint(0, 255), randint(0, 255))

class GameObject:

    def move(self):
        pass
    
    def draw(self, screen):
        pass  


class Shell(GameObject):
    '''
    The ball class. Creates a ball, controls it's movement and implement it's rendering.
    '''
    def __init__(self, coord, vel, rad=20, color=None):
        '''
        Constructor method. Initializes ball's parameters and initial values.
        '''
        self.coord = coord
        self.vel = vel
        if color == None:
            color = rand_color()
        self.color = color
        self.rad = rad
        self.is_alive = True

    def check_corners(self, refl_ort=0.8, refl_par=0.9):
        '''
        Reflects ball's velocity when ball bumps into the screen corners. Implemetns inelastic rebounce.
        '''
        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad
                self.vel[i] = -int(self.vel[i] * refl_ort)
                self.vel[1-i] = int(self.vel[1-i] * refl_par)
            elif self.coord[i] > SCREEN_SIZE[i] - self.rad:
                self.coord[i] = SCREEN_SIZE[i] - self.rad
                self.vel[i] = -int(self.vel[i] * refl_ort)
                self.vel[1-i] = int(self.vel[1-i] * refl_par)

    def move(self, time=1, grav=0):
        '''
        Moves the ball according to it's velocity and time step.
        Changes the ball's velocity due to gravitational force.
        '''
        self.vel[1] += grav
        for i in range(2):
            self.coord[i] += time * self.vel[i]
        self.check_corners()
        if self.vel[0]**2 + self.vel[1]**2 < 2**2 and self.coord[1] > SCREEN_SIZE[1] - 2*self.rad:
            self.is_alive = False

    def draw(self, screen):
        '''
        Adds the background image
        Draws the ball on appropriate surface.
        '''
        #pg.draw.circle(screen, self.color, self.coord, self.rad)
        missle = pg.image.load('missle.png')
       
        screen.blit(missle,self.coord)
              


class Cannon(GameObject):
    '''
    Cannon class. Manages it's renderring, movement and striking.
    '''
    def __init__(self, x_coord, y_coord, coord=[0,0], angle=0, max_pow=50, min_pow=10, color=RED):

        #coord=[30, SCREEN_SIZE[1]//2]
        '''
        Constructor method. Sets coordinate, direction, minimum and maximum power and color of the gun.
        '''
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.coord = [x_coord, y_coord]
        self.angle = angle
        self.max_pow = max_pow
        self.min_pow = min_pow
        self.color = color
        self.active = False
        self.pow = min_pow
    
    def activate(self):
        '''
        Activates gun's charge.
        '''
        self.active = True

    def gain(self, inc=2):
        '''
        Increases current gun charge power.
        '''
        if self.active and self.pow < self.max_pow:
            self.pow += inc

    def strike(self):
        '''
        Creates ball, according to gun's direction and current charge power.
        '''
        vel = self.pow
        angle = self.angle
        ball = Shell(list(self.coord), [int(vel * np.cos(angle)), int(vel * np.sin(angle))])
        self.pow = self.min_pow
        self.active = False
        return ball
        
    def set_angle(self, target_pos):
        '''
        Sets gun's direction to target position.
        '''
        self.angle = np.arctan2(target_pos[1] - self.coord[1], target_pos[0] - self.coord[0])

    def move(self, inc):
        '''
        Changes vertical position of the gun.
        '''
        if (self.coord[1] > 30 or inc > 0) and (self.coord[1] < SCREEN_SIZE[1] - 30 or inc < 0):
            self.coord[1] += inc

    def move_horizontal(self, inc):
        if (self.coord[0] > SCREEN_SIZE[1]//2 or inc > 0) and (self.coord[0] < SCREEN_SIZE[1] - SCREEN_SIZE[1]//2 or inc < 0):
            self.coord[0] += inc

    def draw(self, screen):
        '''
        Adds the tank image, and makes it move along with the gun direction.
        Draws the gun on the screen. 
        '''
        gun_shape = []
        vec_1 = np.array([int(5*np.cos(self.angle - np.pi/2)), int(5*np.sin(self.angle - np.pi/2))])
        vec_2 = np.array([int(self.pow*np.cos(self.angle)), int(self.pow*np.sin(self.angle))])
        gun_pos = np.array(self.coord)
        gun_shape.append((gun_pos + vec_1).tolist())
        gun_shape.append((gun_pos + vec_1 + vec_2).tolist())
        gun_shape.append((gun_pos + vec_2 - vec_1).tolist())
        gun_shape.append((gun_pos - vec_1).tolist())
        pg.draw.polygon(screen, self.color, gun_shape)
        
        #tank image
        tank_image = pg.image.load('tank.png')
        tank_image = pg.transform.scale(tank_image, (100, 100))
        tank_rect = tank_image.get_rect()
        tank_center = np.array([tank_rect.width/2, tank_rect.height/2])
        tank_pos = gun_pos - tank_center
        rotated_tank = pg.transform.rotate(tank_image, np.degrees(self.angle * -1))
        screen.blit(rotated_tank, tank_pos)

    def draw_tank2(self, screen):
        gun_shape = []
        vec_1 = np.array([int(5*np.cos(self.angle - np.pi/2)), int(5*np.sin(self.angle - np.pi/2))])
        vec_2 = np.array([int(self.pow*np.cos(self.angle)), int(self.pow*np.sin(self.angle))])
        gun_pos = np.array(self.coord)
        gun_shape.append((gun_pos + vec_1).tolist())
        gun_shape.append((gun_pos + vec_1 + vec_2).tolist())
        gun_shape.append((gun_pos + vec_2 - vec_1).tolist())
        gun_shape.append((gun_pos - vec_1).tolist())
        pg.draw.polygon(screen, self.color, gun_shape)

        tank_image = pg.image.load('tank.png')
        tank_image = pg.transform.scale(tank_image, (100, 100))
        tank_image = pg.transform.flip(tank_image, False, True)
        tank_rect = tank_image.get_rect()
        tank_center = np.array([tank_rect.width/2, tank_rect.height/2])
        tank_pos = gun_pos - tank_center
        rotated_tank = pg.transform.rotate(tank_image, np.degrees(self.angle * -1))
        screen.blit(rotated_tank, tank_pos)


class Target(GameObject):
    '''
    Target class. Creates target, manages it's rendering and collision with a ball event.
    '''
    def __init__(self, coord=None, color=None, rad=30):
        '''
        Constructor method. Sets coordinate, color and radius of the target.
        '''
        if coord == None:
            coord = [randint(rad, SCREEN_SIZE[0] - rad), randint(rad, SCREEN_SIZE[1] - rad)]
        self.coord = coord
        self.rad = rad

       

        if color == None:
            color = rand_color()
        self.color = color

    def check_collision(self, ball):
        '''
        Checks whether the ball bumps into target.
        '''
        
        dist = sum([(self.coord[i] - ball.coord[i])**2 for i in range(2)])**0.5
        min_dist = self.rad + ball.rad
        return dist <= min_dist
    

    def draw(self, screen):
       # Draws the target on the screen  
            
       #pg.draw.circle(screen, self.color, self.coord, self.rad)

       smile = pg.image.load('smallface.png')
       screen.blit(smile,self.coord)

    def move(self):
        """
        This type of target can't move at all.
        :return: None
        """
        pass

class MovingTargets(Target):
    def __init__(self, coord=None, color=None, rad=30):
        super().__init__(coord, color, rad)
        self.vx = randint(-2, +2)
        self.vy = randint(-2, +2)
    
    def move(self):
        self.coord[0] += self.vx
        self.coord[1] += self.vy


class ScoreTable:
    '''
    Score table class.
    '''
    def __init__(self, t_destr=0, b_used=0):
        self.t_destr = t_destr
        self.b_used = b_used
        self.font = pg.font.SysFont("dejavusansmono", 25)

    def score(self):
        '''
        Score calculation method.
        '''
        return self.t_destr - self.b_used

    def draw(self, screen):
        score_surf = []
        score_surf.append(self.font.render("Destroyed: {}".format(self.t_destr), True, WHITE))
        score_surf.append(self.font.render("Balls used: {}".format(self.b_used), True, WHITE))
        score_surf.append(self.font.render("Total: {}".format(self.score()), True, RED))
        for i in range(3):
            screen.blit(score_surf[i], [10, 10 + 30*i])


class Manager:
    '''
    Class that manages events' handling, ball's motion and collision, target creation, etc.
    '''
    def __init__(self, n_targets=1):
        self.balls = []
        self.gun = Cannon(30, SCREEN_SIZE[1]//2)
        self.gun2 = Cannon(SCREEN_SIZE[1] + 200, SCREEN_SIZE[1]//2)
        self.targets = []
        self.score_t = ScoreTable()
        self.n_targets = n_targets
        self.new_mission()

    def new_mission(self):
        '''
        Adds new targets.
        '''
        for i in range(self.n_targets):
            self.targets.append(MovingTargets(rad=randint(max(1, 30 - 2*max(0, self.score_t.score())),
                30 - max(0, self.score_t.score()))))
            self.targets.append(Target(rad=randint(max(1, 30 - 2*max(0, self.score_t.score())),
                30 - max(0, self.score_t.score()))))


    def process(self, events, screen):
        '''
        Runs all necessary method for each iteration. Adds new targets, if previous are destroyed.
        '''
        done = self.handle_events(events)

        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.gun.set_angle(mouse_pos)
            self.gun2.set_angle(mouse_pos)
        
        self.move()
        self.collide()
        self.draw(screen)
        

        if len(self.targets) == 0 and len(self.balls) == 0:
            self.new_mission()

        return done

    def handle_events(self, events):
        '''
        Handles events from keyboard, mouse, etc.
        '''

        done = False
        for event in events:
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.gun.move(-5)
                    self.gun2.move(-5)
                elif event.key == pg.K_DOWN:
                    self.gun.move(5)
                    self.gun2.move(5)
                elif event.key == pg.K_RIGHT:
                    self.gun.move_horizontal(5)
                    self.gun2.move_horizontal(5)
                elif event.key == pg.K_LEFT:
                    self.gun.move_horizontal(-5)
                    self.gun2.move_horizontal(-5)
            elif event.type == pg.MOUSEBUTTONDOWN:
                circles.add(Bombs((randint(1,700),10), screen))

                if event.button == 1:
                    self.gun.activate()
                    self.gun2.activate()
            elif event.type == pg.MOUSEBUTTONUP:

                if event.button == 1:
                    self.balls.append(self.gun.strike())
                    self.balls.append(self.gun2.strike())
                    self.score_t.b_used += 1
        return done

    def draw(self, screen):
        '''
        Runs balls', gun's, targets' and score table's drawing method.
        '''
        screen.blit(background, (0,0))
        for ball in self.balls:
            ball.draw(screen)
        for target in self.targets:
            target.draw(screen)
        self.gun.draw(screen)
        self.gun2.draw_tank2(screen)
        self.score_t.draw(screen)

    def move(self):
        '''
        Runs balls' and gun's movement method, removes dead balls.
        '''
        dead_balls = []
        for i, ball in enumerate(self.balls):
            ball.move(grav=2)
            if not ball.is_alive:
                dead_balls.append(i)
        for i in reversed(dead_balls):
            self.balls.pop(i)
        for i, target in enumerate(self.targets):
            target.move()
        self.gun.gain()
        self.gun2.gain()

    def collide(self):
        '''
        Checks whether balls bump into targets, sets balls' alive trigger.
        '''
        collisions = []
        targets_c = []
        for i, ball in enumerate(self.balls):
            for j, target in enumerate(self.targets):
                if target.check_collision(ball):
                    collisions.append([i, j])
                    targets_c.append(j)
        targets_c.sort()
        for j in reversed(targets_c):
            self.score_t.t_destr += 1
            self.targets.pop(j)

GRAVITY = .5  # Pretty low gravity.

class Bombs(pg.sprite.Sprite):

    def __init__(self, pos, screen):
        super().__init__()
        self.screen = screen
        self.image = pg.Surface((80, 80), pg.SRCALPHA)
        pg.draw.circle(self.image, RED, (40, 40), 10)
        self.rect = self.image.get_rect(center=pos)
        self.pos_y = pos[1]
        self.speed_y = 0

    def update(self):
        self.speed_y += GRAVITY
        self.pos_y += self.speed_y
        self.rect.y = self.pos_y

        if self.pos_y > self.screen.get_height():
            self.kill() 
           


screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("The gun of Khiryanov")

done = False
clock = pg.time.Clock()

mgr = Manager(n_targets=3)
circles = pg.sprite.Group(Bombs((600, 0), screen))

while not done:
    clock.tick(15)
    screen.fill(BLACK)
    circles.update()
    done = mgr.process(pg.event.get(), screen)
    circles.draw(screen)
    pg.display.flip()
    clock.tick(60)
 
pg.quit()