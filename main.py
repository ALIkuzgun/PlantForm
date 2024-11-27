import pygame, random
from pygame import BLEND_RGB_ADD
from map import *

class Wall():
    def __init__(self, x, y, en, boy):        
        self.x = x      
        self.y = y
        self.en = en
        self.boy = boy
        self.rect = pygame.Rect(x, y, self.en, self.boy)

    def draw(self):
        pygame.draw.rect(ekran,(244,122,122),self.rect)

class Map():
    def __init__(self, x, y):        
        self.image = pygame.image.load('img/platform_game_map.png')
        self.rect = pygame.Rect(x, y, 2240, 2240)

    def draw(self):
        ekran.blit(self.image,self.rect)

class Plants():
    def __init__(self, x, y, img_type):        
        self.img_type = img_type
        self.image = pygame.image.load(f'img/{self.img_type}.png')
        self.rect = pygame.Rect(x, y, 32, 32)

    def draw(self):
        ekran.blit(self.image,self.rect)

class Dark():
    def __init__(self, x, y):        
        self.image = pygame.image.load('img/game_dark.png')
        self.rect = pygame.Rect(x, y, 800, 660)

    def draw(self):
        self.rect.y = player.rect.centery-830
        self.rect.x = player.rect.centerx-980
        ekran.blit(self.image,self.rect)

class Slime():
    def __init__(self, x, y, en, boy, speed):  
        self.images = {
            'idle': pygame.image.load('img/enemy/platform_slime.png'),
            'idle2': pygame.image.load('img/enemy/platform_slime2.png')
        }
        self.endimage = self.images["idle"].subsurface(pygame.Rect(226, 8, 28, 24)) 
        self.x, self.y = x, y
        self.en, self.boy = en, boy
        self.rect = pygame.Rect(self.x, self.y, self.en, self.boy)
        self.speed = speed
        self.gravity = 0.5  
        self.vertical_speed = 0  
        self.on_ground = False  
        self.move_direction, self.move_status = "right",  0
        self.attack = 0
        self.attack_animation_time = 0
        self.animation_time = 0
        self.health = 50
        self.animation_frame = 0
        self.attack_animation_frame = 0
        self.attack_rect = pygame.Rect(10000, 1000, 30, 30)
        self.right_imgs = [(292, 40, 28, 24), (260, 40, 28, 24), (228, 40, 28, 24),
                           (194, 40, 28, 24), (160, 40, 28, 24), (128, 40, 28, 24), (98, 40, 28, 24)]
        self.left_imgs = [(292, 40, 28, 24), (260, 40, 28, 24), (228, 40, 28, 24),
                          (194, 40, 28, 24), (160, 40, 28, 24), (128, 40, 28, 24), (98, 40, 28, 24)]
        
    def apply_gravity(self, walls):
        if not self.on_ground:
            self.vertical_speed += self.gravity
        else:
            self.vertical_speed = 0 
        self.rect.y += self.vertical_speed

        self.on_ground = False
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if self.vertical_speed > 0:
                    self.rect.bottom = wall.rect.top  
                    self.on_ground = True

    def move(self):
        moving_horizontally = False
        moving_vertically = False
        original_position = self.rect.topleft

        distance_threshold = 250 
        if abs(player.rect.x - self.rect.x) <= distance_threshold and abs(player.rect.y - self.rect.y) <= distance_threshold:
            if player.rect.x > self.rect.x:
                self.rect.x += 2
                self.move_direction = "right"
                moving_horizontally = True
            if player.rect.x < self.rect.x:
                self.rect.x -= 2
                self.move_direction = "left"
                moving_horizontally = True

        if moving_horizontally or moving_vertically:
            self.move_status = 1
        else:
            self.move_status = 0

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.topleft = original_position
                moving_horizontally = False
                moving_vertically = False
                self.move_status = 0
                break

        if self.move_status == 1:
            self.animation_time += 1
            if self.move_direction == "right":
                if self.animation_time >= 10:
                    self.animation_frame = (self.animation_frame + 1) % len(self.right_imgs)
                    frame_rect = pygame.Rect(self.right_imgs[self.animation_frame])
                    self.endimage = self.images["idle2"].subsurface(frame_rect)
                    self.animation_time = 0
            elif self.move_direction == "left":
                if self.animation_time >= 10:
                    self.animation_frame = (self.animation_frame + 1) % len(self.left_imgs)
                    frame_rect = pygame.Rect(self.left_imgs[self.animation_frame])
                    self.endimage = self.images["idle"].subsurface(frame_rect)
                    self.animation_time = 0
        else:  
            if self.move_direction == "right" or player.rect.x > self.rect.x and player.rect.y > self.rect.y:
                self.endimage = self.images["idle2"].subsurface(pygame.Rect(226, 8, 28, 24)) 
            elif self.move_direction == "left" or player.rect.x < self.rect.x and player.rect.y > self.rect.y:
                self.endimage = self.images["idle"].subsurface(pygame.Rect(226, 8, 28, 24))

    def draw_health_bar(self):
        pygame.draw.rect(ekran, (0, 0, 0), (self.rect.x-14, self.rect.y-17, 54, 14))
        pygame.draw.rect(ekran, (255, 0, 0), (self.rect.x-12, self.rect.y-15, 50, 10))
        pygame.draw.rect(ekran, (0, 255, 0), (self.rect.x-12, self.rect.y-15, self.health, 10))

    def draw(self):
        ekran.blit(self.endimage, self.rect)

    def player_attack_hit(self):
        if self.rect.colliderect(attack.rect):
            self.health -= 5.5
            if player.direction == "right":
              self.rect.x += 35
            if player.direction == "left":
              self.rect.x -= 35
        for slime in slimies:
            if slime.health <= 0:
                slimies.remove(slime)

    def update(self, walls):
        self.apply_gravity(walls)
        self.draw()
        self.draw_health_bar()
        self.player_attack_hit()
        self.move()

class Player():
    def __init__(self, x, y, en, boy, speed):  
        self.images = {
            'idle': pygame.image.load('img/player/Meow-Knight_Idle.png'),
            'idle2': pygame.image.load('img/player/Meow-Knight_Idle2.png'),
            'jump': pygame.image.load('img/player/Meow-Knight_Jump.png'),
            'walk': pygame.image.load('img/player/Meow-Knight_Run.png'),
            'walk2': pygame.image.load('img/player/Meow-Knight_Run2.png'),
            'attack': pygame.image.load('img/player/Meow-Attack2.png'),
            'attack2': pygame.image.load('img/player/Meow_Attack2-Left.png')
        }
        self.endimage = self.images["idle"].subsurface(pygame.Rect(4, 2, 24, 30)) 
        self.x = x
        self.y = y
        self.en = en
        self.boy = boy
        self.rect = pygame.Rect(self.x, self.y, self.en, self.boy)
        self.speed = speed
        self.velocity_y = 0  
        self.velocity_x = 0  
        self.on_ground = False 
        self.move_direction = "stay"
        self.direction = "right"
        self.player_wall_hit = 0
        self.move_status = 0
        self.plant_number = 0
        self.health = 200
        self.attack = 0
        self.wall_passage_hit = 0
        self.wall_passage2_hit = 0
        self.mushroom_time, self.mushroom_hit = 0, 0
        self.mushroom_img = pygame.image.load('img/mushroom.png')
        self.fly_trap_time, self.fly_trap_hit = 0, 0
        self.fly_trap_img = pygame.image.load('img/fly_trap.png')
        self.arctic_willow_time, self.arctic_willow_hit = 0, 0
        self.arctic_willow_img = pygame.image.load('img/arctic_willow.png')
        self.rafflesia_flower_time, self.rafflesia_flower_hit = 0, 0
        self.rafflesia_flower_img = pygame.image.load('img/rafflesia_flower.png')
        self.super_mario_flower_time, self.super_mario_flower_hit = 0, 0
        self.super_mario_flower_img = pygame.image.load('img/super_mario_flower.png')
        self.tulip_time, self.tulip_hit = 0, 0
        self.tulip_img = pygame.image.load('img/tulip.png')
        self.animation_time, self.animation_frame = 0, 0
        self.game_win = 0
        self.time = 0
        self.cat_right_down_imgs,self.cat_left_down_imgs = [(4, 4, 24, 28),(4, 52, 22, 30),(4, 134, 24, 30),(4, 188, 22, 32),(4, 244, 24, 28),(4, 292, 24, 30),(4, 374, 26, 30),(4, 428, 24, 32)],[(4, 4, 24, 28),(4, 52, 22, 30),(4, 134, 24, 30),(4, 188, 22, 32),(4, 244, 24, 28),(4, 292, 24, 30),(4, 374, 26, 30),(4, 428, 24, 32)]

    def move(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
           self.attack = 1

        if key[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.move_direction = "right"
            self.direction = "right"
            self.move_status = 1
            self.attack = 0
        elif key[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.move_direction = "left"
            self.direction = "left"
            self.move_status = 1
            self.attack = 0
        else:
            self.move_direction = "stay"
            self.move_status = 0

        if self.rect.x >= width-300:
            self.rect.x = width-300

        if self.rect.x <= 300:
            self.rect.x = 300

        if key[pygame.K_UP] and self.on_ground:
            self.velocity_y = -15 

        self.velocity_y += 1  
        if self.velocity_y > 10:
            self.velocity_y = 10

        self.rect.y += self.velocity_y  

        if self.rect.y + self.boy >= height:  
            self.rect.y = height - self.boy
            self.on_ground = True
            self.velocity_y = 0
        else:
            self.on_ground = False
          
        if self.move_status == 1:
            self.animation_time += 1
            if self.move_direction == "right":
                if self.animation_time >= 8:
                    self.animation_frame = (self.animation_frame + 1) % len(self.cat_right_down_imgs)
                    frame_rect = pygame.Rect(self.cat_right_down_imgs[self.animation_frame])
                    self.endimage = self.images["walk"].subsurface(frame_rect)
                    self.animation_time = 0
            elif self.move_direction == "left":
                if self.animation_time >= 8:
                    self.animation_frame = (self.animation_frame + 1) % len(self.cat_left_down_imgs)
                    frame_rect = pygame.Rect(self.cat_left_down_imgs[self.animation_frame])
                    self.endimage = self.images["walk2"].subsurface(frame_rect)
                    self.animation_time = 0
        else:
            if self.direction == "right":
                self.endimage = self.images["idle"].subsurface(pygame.Rect(4, 2, 24, 30))
            elif self.direction == "left":
                self.endimage = self.images["idle2"].subsurface(pygame.Rect(4, 2, 24, 30))

        if self.attack == 1:
            if self.move_direction == "stay":
                self.animation_time += 1
                if self.direction == "right":
                    if self.animation_time >= 5:
                        self.endimage = self.images["attack"].subsurface(pygame.Rect(4, 336, 58, 32))
                        attack.rect.x,attack.rect.y = self.rect.x+self.en+5,self.rect.y+10
                    if self.animation_time >= 15:
                        self.endimage = self.images["attack"].subsurface(pygame.Rect(4, 388, 58, 32))
                        attack.rect.x,attack.rect.y = self.rect.x+self.en+5,self.rect.y+10
                    if self.animation_time >= 25:
                        self.endimage = self.images["attack"].subsurface(pygame.Rect(4, 440, 58, 32))
                        attack.rect.x,attack.rect.y = self.rect.x+self.en+5,self.rect.y+10
                    if self.animation_time >= 35:
                        self.animation_time = 0
                        self.attack = 0
                elif self.direction == "left":
                    if self.animation_time >= 5:
                        self.endimage = self.images["attack2"].subsurface(pygame.Rect(4, 336, 58, 32))
                        attack.rect.x,attack.rect.y = self.rect.x-3,self.rect.y+10
                    if self.animation_time >= 15:
                        self.endimage = self.images["attack2"].subsurface(pygame.Rect(4, 388, 58, 32))
                        attack.rect.x,attack.rect.y = self.rect.x-3,self.rect.y+10
                    if self.animation_time >= 25:
                        self.endimage = self.images["attack2"].subsurface(pygame.Rect(4, 440, 58, 32))
                        attack.rect.x,attack.rect.y = self.rect.x-3,self.rect.y+10
                    if self.animation_time >= 35:
                        self.animation_time = 0
                        self.attack = 0
        else:
            attack.rect.x,attack.rect.y = 1000,1000

    def wall_hit(self):
        self.player_wall_hit = 0  
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if self.velocity_y > 0 and self.rect.bottom > wall.rect.top and self.rect.top < wall.rect.top:
                    self.rect.bottom = wall.rect.top
                    self.on_ground = True
                    self.velocity_y = 0

                elif self.velocity_y < 0 and self.rect.top < wall.rect.bottom and self.rect.bottom > wall.rect.bottom:
                    self.rect.top = wall.rect.bottom
                    self.velocity_y = 0

                elif self.rect.right > wall.rect.left and self.rect.left < wall.rect.left:
                    self.rect.right = wall.rect.left
                    self.player_wall_hit = 1

                elif self.rect.left < wall.rect.right and self.rect.right > wall.rect.right:
                    self.rect.left = wall.rect.right
                    self.player_wall_hit = 1

        for wall_kill in walls_kill:
            global player_died
            if self.rect.colliderect(wall_kill.rect):
                self.health = 0

        for wall_passage in walls_passage:
            if self.rect.colliderect(wall_passage.rect):
              self.wall_passage_hit = 1

            if self.wall_passage_hit == 1:
              if map.rect.y >= -800:
                map.rect.y -= 0.1
                for spritie_list in sprities_list:
                  for spritiex_list in spritie_list:
                    spritiex_list.rect.y -= 4
                for spritie in sprities:
                    spritie.rect.y -= 4
              else:
                self.wall_passage_hit = 0
                for wall in walls:
                   self.rect.y = 100

        for wall_passage2 in walls_passage2:
            if self.rect.colliderect(wall_passage2.rect):
              self.wall_passage2_hit = 1

            if self.wall_passage2_hit == 1:
              if map.rect.y >= -1600:
                map.rect.y -= 0.1
                for spritie_list in sprities_list:
                  for spritiex_list in spritie_list:
                    spritiex_list.rect.y -= 4
                for spritie in sprities:
                    spritie.rect.y -= 4
              else:
                self.wall_passage2_hit = 0
                for wall in walls:
                   self.rect.y = 100

    def particle_draw(self):
            if random.random() < 0.6:
                particles.append([[406,240], [random.uniform(-2, 2), random.uniform(-5, -2)], random.randint(5, 10)])
            for particle in particles[:]:
                particle[0][0] += particle[1][0]  
                particle[0][1] += particle[1][1]  
                particle[2] -= 0.1
                particle[1][1] += 0.1  
                radius = int(particle[2])
                if radius > 0:
                    ekran.blit(circle_surf(radius, (255, 255, 255)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=BLEND_RGB_ADD)
                else:
                    particles.remove(particle)

    def plants_hit(self):
        if self.rect.colliderect(mushroom.rect):
            self.plant_number += 1
            mushroom.rect.x = 10000
            self.mushroom_hit = 1
        if self.mushroom_hit == 1:
          self.mushroom_time += 1
          if self.mushroom_time <= 100:
            ekran.blit(dark_surface, (0, 0))
            self.mushroom_img = pygame.transform.scale(self.mushroom_img, (128,128))
            self.particle_draw()
            ekran.blit(self.mushroom_img,(338,220))
            tp = pygame.font.Font('Teko-Medium.ttf', 50).render('Mushroom found',True,(255,255,255))
            ekran.blit(tp,(275,365))    
          else:
            self.mushroom_hit = 0
       
        if self.rect.colliderect(fly_trap.rect):
            self.plant_number += 1
            fly_trap.rect.x = 10000
            self.fly_trap_hit = 1
        if self.fly_trap_hit == 1:
          self.fly_trap_time += 1
          if self.fly_trap_time <= 100:
            ekran.blit(dark_surface, (0, 0))
            self.fly_trap_img = pygame.transform.scale(self.fly_trap_img, (128,128))
            self.particle_draw()
            ekran.blit(self.fly_trap_img,(338,220))
            tp = pygame.font.Font('Teko-Medium.ttf', 50).render('Fly Trap found',True,(255,255,255))
            ekran.blit(tp,(290,365))    
          else:
            self.fly_trap_hit = 0
       
        if self.rect.colliderect(arctic_willow.rect):
            self.plant_number += 1
            arctic_willow.rect.x = 10000
            self.arctic_willow_hit = 1
        if self.arctic_willow_hit == 1:
          self.arctic_willow_time += 1
          if self.arctic_willow_time <= 100:
            ekran.blit(dark_surface, (0, 0))
            self.arctic_willow_img = pygame.transform.scale(self.arctic_willow_img, (128,128))
            self.particle_draw()
            ekran.blit(self.arctic_willow_img,(338,220))
            tp = pygame.font.Font('Teko-Medium.ttf', 50).render('Arctic Willow found',True,(255,255,255))
            ekran.blit(tp,(250,365))    
          else:
            self.arctic_willow_hit = 0

        if self.rect.colliderect(rafflesia_flower.rect):
            self.plant_number += 1
            rafflesia_flower.rect.x = 10000
            self.rafflesia_flower_hit = 1
        if self.rafflesia_flower_hit == 1:
          self.rafflesia_flower_time += 1
          if self.rafflesia_flower_time <= 100:
            ekran.blit(dark_surface, (0, 0))
            self.rafflesia_flower_img = pygame.transform.scale(self.rafflesia_flower_img, (128,128))
            self.particle_draw()
            ekran.blit(self.rafflesia_flower_img,(338,220))
            tp = pygame.font.Font('Teko-Medium.ttf', 50).render('Rafflesia Flower found',True,(255,255,255))
            ekran.blit(tp,(220,365))    
          else:
            self.rafflesia_flower_hit = 0

        if self.rect.colliderect(super_mario_flower.rect):
            self.plant_number += 1
            super_mario_flower.rect.x = 10000
            self.super_mario_flower_hit = 1
        if self.super_mario_flower_hit == 1:
          self.super_mario_flower_time += 1
          if self.super_mario_flower_time <= 100:
            ekran.blit(dark_surface, (0, 0))
            self.super_mario_flower_img = pygame.transform.scale(self.super_mario_flower_img, (128,128))
            self.particle_draw()
            ekran.blit(self.super_mario_flower_img,(338,220))
            tp = pygame.font.Font('Teko-Medium.ttf', 50).render('Super Mario Flower found',True,(255,255,255))
            ekran.blit(tp,(200,365))    
          else:
            self.super_mario_flower_hit = 0

        if self.rect.colliderect(tulip.rect):
            self.plant_number += 1
            tulip.rect.x = 10000
            self.tulip_hit = 1
        if self.tulip_hit == 1:
          self.tulip_time += 1
          if self.tulip_time <= 100:
            ekran.blit(dark_surface, (0, 0))
            self.tulip_img = pygame.transform.scale(self.tulip_img, (128,128))
            self.particle_draw()
            ekran.blit(self.tulip_img,(338,220))
            tp = pygame.font.Font('Teko-Medium.ttf', 50).render('Tulip found',True,(255,255,255))
            ekran.blit(tp,(310,365))    
          else:
            self.tulip_hit = 0

    def slime_hit(self):
        for slime in slimies:
            if self.rect.colliderect(slime.rect):
                self.health -= 1.3

    def win(self):
        if self.plant_number >= 6:
            self.time += 1
           
        if self.time >= 140:
            global game
            game = 0
            ekran.blit(dark_surface2, (0, 0))
            tp = pygame.font.Font('Teko-Medium.ttf', 90).render('Game Over',True,(255,255,255))
            tp2 = pygame.font.Font('Teko-Medium.ttf', 90).render('Thank You For Playing',True,(255,255,255))
            ekran.blit(tp,(240,165))    
            ekran.blit(tp2,(90,275))    

    def draw(self):
        ekran.blit(self.endimage,self.rect)

    def draw_health_bar(self):
        pygame.draw.rect(ekran,(0,255,0),(10,10,self.health,20))

    def update(self):
        self.draw()
        self.slime_hit()
        self.wall_hit()
        self.move()

class Attack():
    def __init__(self,x,y,en,boy):  
        self.x = x
        self.y = y
        self.en = en
        self.boy = boy
        self.rect = pygame.Rect(self.x, self.y, self.en, self.boy)

    def draw(self):
        pygame.draw.rect(ekran,(0,220,0),self.rect)

pygame.init()

game = 1
game_status = 0
player_died = 0
start_button = pygame.Rect(180,360,160,60)
exit_button = pygame.Rect(480,360,160,60)
pg_button = pygame.Rect(280,320,240,60)
exit_button2 = pygame.Rect(322,420,160,60)

width, height= 800, 630
ekran = pygame.display.set_mode((width,height))
pygame.display.set_caption('plantform')
clock = pygame.time.Clock()

sprities = []
sprities_list = []
particles = []

dark_surface = pygame.Surface((width, height))
dark_surface.fill((0, 0, 0)) 
dark_surface.set_alpha(158) 
dark_surface2 = pygame.Surface((width, height))
dark_surface2.fill((0, 0, 0)) 
dark_surface2.set_alpha(200) 

map = Map(0,0)
dark = Dark(0,0)
player = Player(x=width//2-120,y=height//2,en=24,boy=30,speed=4)
attack = Attack(player.x,player.y,25,15)
mushroom = Plants(1990,525,"mushroom")
fly_trap = Plants(3570,54,"fly_trap")
arctic_willow = Plants(4695,896,"arctic_willow")
rafflesia_flower = Plants(2436,1227,"rafflesia_flower")
super_mario_flower = Plants(1176,1910,"super_mario_flower")
tulip = Plants(5460,1694,"tulip")

def create_walls(wall_map):
    walls = []
    walls_passage = []
    cell_size = 42
    for y, row in enumerate(wall_map):
        for x, value in enumerate(row):
            if value == 1: 
                wall = Wall(x * cell_size, y * cell_size, cell_size, cell_size)
                walls.append(wall)
            if value == 2: 
                wall = Wall(x * cell_size, y * cell_size+10, cell_size, cell_size)
                walls.append(wall)
    return walls

def create_walls_kill(wall_map):
    walls_kill = []
    cell_size = 42
    for y, row in enumerate(wall_map):
        for x, value in enumerate(row):
            if value == 3: 
                wall_kill = Wall(x * cell_size, y * cell_size+10, cell_size, cell_size)
                walls_kill.append(wall_kill)
    return walls_kill

def create_walls_passage(wall_map):
    walls_passage = []
    cell_size = 42
    for y, row in enumerate(wall_map):
        for x, value in enumerate(row):
            if value == 4: 
                wall_passage = Wall(x * cell_size, y * cell_size+10, cell_size, cell_size)
                walls_passage.append(wall_passage)
    return walls_passage

def create_walls_passage2(wall_map):
    walls_passage2 = []
    cell_size = 42
    for y, row in enumerate(wall_map):
        for x, value in enumerate(row):
            if value == 5: 
                wall_passage2 = Wall(x * cell_size, y * cell_size+10, cell_size, cell_size)
                walls_passage2.append(wall_passage2)
    return walls_passage2

def create_slime(wall_map):
    slimies = []
    cell_size = 42
    for y, row in enumerate(wall_map):
        for x, value in enumerate(row):
            if value == 9: 
                slime = Slime(x * cell_size, y * cell_size+10, 28, 24,3)
                slimies.append(slime)
    return slimies

walls = create_walls(wall_map)
walls_kill = create_walls_kill(wall_map)
walls_passage = create_walls_passage(wall_map)
walls_passage2 = create_walls_passage2(wall_map)
slimies = create_slime(wall_map)
sprities.append(map)
sprities.append(mushroom)
sprities.append(fly_trap)
sprities.append(arctic_willow)
sprities.append(rafflesia_flower)
sprities.append(super_mario_flower)
sprities.append(tulip)
sprities_list.append(walls)
sprities_list.append(walls_kill)
sprities_list.append(walls_passage)
sprities_list.append(walls_passage2)
sprities_list.append(slimies)

def circle_surf(radius, color):
    surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(surface, color, (radius, radius), radius)
    return surface

def particle_draw():
    if random.random() < 0.1:
        particles.append([[player.rect.x, player.rect.y+player.boy], [random.uniform(-2, 2), random.uniform(-5, -2)], random.randint(5, 10)])
    for particle in particles[:]:
        particle[0][0] += particle[1][0]  
        particle[0][1] += particle[1][1]  
        particle[2] -= 0.1  
        particle[1][1] += 0.1  
        radius = int(particle[2])
        if radius > 0:
            ekran.blit(circle_surf(radius, (255, 255, 255)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=BLEND_RGB_ADD)
        else:
            particles.remove(particle)

def camera():
    if player.player_wall_hit == 0:
        if player.move_direction == "right":
            for spritie in sprities:
                spritie.rect.x -= player.speed
            for spritiex in sprities_list:
              for spritie in spritiex:
                spritie.rect.x -= player.speed
        if player.move_direction == "left":
            for spritie in sprities:
                spritie.rect.x += player.speed
            for spritiex in sprities_list:
              for spritie in spritiex:
                spritie.rect.x += player.speed
 
def beginning():
    if game_status == 0:
        ekran.blit(dark_surface2, (0, 0))
        tp = pygame.font.Font('Teko-Medium.ttf', 100).render('Plantformer',True,(255,255,255))
        tp2 = pygame.font.Font('Teko-Medium.ttf', 40).render('*The aim of the game is to find the 6 plants in the game.',True,(255,255,255))
        tp3 = pygame.font.Font('Teko-Medium.ttf', 60).render('START',True,(255,255,255))
        tp4 = pygame.font.Font('Teko-Medium.ttf', 60).render('EXIT',True,(255,255,255))
        ekran.blit(tp, (220, 110))
        ekran.blit(tp2, (50, 550))
        pygame.draw.rect(ekran,(102,102,102),start_button,border_radius=20)
        pygame.draw.rect(ekran,(102,102,102),exit_button,border_radius=20)
        ekran.blit(tp3, (200, 350))
        ekran.blit(tp4, (520, 350))

def died():
    global player_died
    if player.health <= 0:
        player_died = 1
        ekran.blit(dark_surface2, (0, 0))
        tp = pygame.font.Font('Teko-Medium.ttf', 100).render('You Died',True,(255,255,255))
        tp3 = pygame.font.Font('Teko-Medium.ttf', 60).render('Play Again',True,(255,255,255))
        tp4 = pygame.font.Font('Teko-Medium.ttf', 60).render('EXIT',True,(255,255,255))
        ekran.blit(tp, (260, 110))
        pygame.draw.rect(ekran,(102,102,102),pg_button,border_radius=20)
        pygame.draw.rect(ekran,(102,102,102),exit_button2,border_radius=20)
        ekran.blit(tp3, (300, 310))
        ekran.blit(tp4, (358, 410))

def resart():
    global game, map ,player, mushroom, fly_trap, arctic_willow, rafflesia_flower, super_mario_flower, tulip, slimies, walls, walls_kill, walls_passage, walls_passage2
    map = Map(0,0)
    game = 1
    player = Player(x=width // 2 - 120, y=height // 2, en=24, boy=30, speed=4)
    mushroom = Plants(1990,525,"mushroom")
    fly_trap = Plants(3570,65,"fly_trap")
    arctic_willow = Plants(4704,907,"arctic_willow")
    rafflesia_flower = Plants(2794,1223,"rafflesia_flower")
    super_mario_flower = Plants(1176,1910,"super_mario_flower")
    tulip = Plants(5460,170,"tulip")
    walls = create_walls(wall_map)
    walls_kill = create_walls_kill(wall_map)
    walls_passage = create_walls_passage(wall_map)
    walls_passage2 = create_walls_passage2(wall_map)
    slimies = create_slime(wall_map)
    sprities.clear()
    sprities.append(map)
    sprities.append(mushroom)
    sprities.append(fly_trap)
    sprities.append(arctic_willow)
    sprities.append(rafflesia_flower)
    sprities.append(super_mario_flower)
    sprities.append(tulip)
    sprities_list.clear()
    sprities_list.append(walls)
    sprities_list.append(walls_kill)
    sprities_list.append(walls_passage)
    sprities_list.append(walls_passage2)
    sprities_list.append(slimies)
    global player_died
    player_died = 0
    player.plant_number = 0
    player.health = 200

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if player_died == 1:
                if pg_button.collidepoint(mouse_pos):
                    player_died = 0
                    game = 0
                    resart()
                if exit_button2.collidepoint(mouse_pos):
                    run = False
            if game_status == 0:
                if start_button.collidepoint(mouse_pos):
                    game_status = 1
                if exit_button.collidepoint(mouse_pos):
                    run = False

    ekran.fill((0,0,0))
    camera()
    map.draw()
    beginning()
    if game_status == 1:
        mushroom.draw()
        fly_trap.draw()
        arctic_willow.draw()
        rafflesia_flower.draw()
        super_mario_flower.draw()
        tulip.draw()
        if game == 1:
            player.update()    
            for slime in slimies:
              slime.update(walls)     
            dark.draw()
        player.plants_hit()
        player.draw_health_bar()
        player.win()
    died()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()