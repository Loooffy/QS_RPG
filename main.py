import arcade
import random
import math
import ui
from config import *

SIZE = WIDTH , HEIGHT = 1440,900
TITLE = "Hi arcade"
BACKGROUND_COLOR = arcade.color.WHITE
FPS = 60

DIRECTIONS = ["up","right","down","left"]
TRANSPORT = {(720,450):(450,720)}
"""
def in_sector(x,y,center_x,center_y,degree,sector_degree=45): # 0 < = degree < 360 ,degree = 0 mean face west , 90 mean face north
    def radian(degree):
        return degree/180*math.pi
    def in_right_border():
        right_border_degree = degree + sector_degree
        right_border_degree -= 360 if right_border_degree >= 360 else 0 
        if right_border_degree % 90 == 0:
            if factor_y > 0:
                factor_y = 1
                factor_x = 0
                value = center_y
            else :
                factor_y = 0
                factor_x = 1
                value = center_x
        else:
            factor_y = 1
            factor_x = math.tan(radian(right_border_degree))
            value = center_x - center_y
        if right_border_degree < 180 :
            return factor_x * x + factor_y * y <= value
        else:
            return factor_x * x + factor_y * y >= value
    def in_left_border():
        left_border_degree = degree - sector_degree
        left_border_degree += 360 if left_border_degree < 0 else 0 
        if left_border_degree % 90 == 0:
            if factor_y > 0:
                factor_y = 1
                factor_x = 0
                value = center_y
            else :
                factor_y = 0
                factor_x = 1
                value = center_x
        else:
            factor_y = 1
            factor_x = math.tan(radian(left_border_degree))
            value = center_x - center_y
        if left_border_degree < 180 :
            return factor_x * x + factor_y * y <= value
        else:
            return factor_x * x + factor_y * y >= value
    print(in_right_border())
    print(in_left_border())
    return in_right_border() and in_left_border()
"""
def get_distance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)
def degree(radian):
        return radian*180/math.pi
def radian(degree):
    return degree*math.pi/180
def atan_to_degree(delta_x,delta_y):
    if delta_y > 0:
        if delta_x >= 0:
            az = 90 - degree(math.atan(delta_x/delta_y))
        else:
            az = degree(math.atan(abs(delta_x)/delta_y)) + 90
    elif delta_y < 0:
        if delta_x < 0:
            az = degree(math.atan(delta_x/abs(delta_y))) + 270
        else:
            az = degree(math.atan(delta_x/abs(delta_y))) + 270
    else:
        if delta_x > 0:
            az= 0
        elif delta_x < 0:
            az = 180
        else :
            az = None
    return az
def in_sector(x,y,center_x,center_y,direction,sector_degree=45):
    delta_x = x - center_x
    delta_y = y - center_y
    az = atan_to_degree(delta_x,delta_y)
    if az != None:
        return not sector_degree < abs(direction-az) < 360 - sector_degree
    return False
def polar_coordinate_to_cartesian(degree,distance,center_x,center_y):
    if degree%360 == 90:
        return center_x , center_y + distance
    elif degree%360 == 270:
        return center_x , center_y - distance
    else:
        return center_x + math.cos(radian(degree)) * distance , center_y + math.sin(radian(degree)) *distance

class Player(arcade.Sprite):
    def __init__(self,begin_x,begin_y,attack,defence,health,speed,atkrange=150):
        super().__init__()
        self.textures=arcade.load_spritesheet('./image/player_moves.png',96,96,4,16)
        self.step=0
        self.dir_textures={
            (270,'in_motion'):[self.textures[0],self.textures[1],self.textures[2],self.textures[3]],
            (0,'in_motion'):[self.textures[4],self.textures[5],self.textures[6],self.textures[7]],
            (90,'in_motion'):[self.textures[8],self.textures[9],self.textures[10],self.textures[11]],
            (180,'in_motion'):[self.textures[12],self.textures[13],self.textures[14],self.textures[15]],
            (270,'idle'):[self.textures[3],self.textures[3],self.textures[3],self.textures[3]],
            (0,'idle'):[self.textures[7],self.textures[7],self.textures[7],self.textures[7]],
            (90,'idle'):[self.textures[11],self.textures[11],self.textures[11],self.textures[11]],
            (180,'idle'):[self.textures[15],self.textures[15],self.textures[15],self.textures[15]]
            }
        self.texture=self.dir_textures[90,'idle'][0]
        self.direction = 270 # direction=0 => face east ,counter clockwise
        self.status='idle' # status = "idle" or "in_motion"
        self.center_x = begin_x
        self.center_y = begin_y
        self.attack = attack
        self.defence = defence
        self.maxhealth = health
        self.health = health
        self.atkrange = 150
        self.speed = speed*60/FPS
        self.change_x = 0
        self.change_y = 0
        self.possession = arcade.SpriteList()
        self.career = "mage"
        #gunner set up
        self.bullet_begin_distance_with_player = 50
        self.bullet_speed = 5*60/FPS
        self.gunner_atkrange = 350
        #mage set up
        self.fireball_begin_distance_with_player = 50
        self.fireball_speed = 5*60/FPS
        self.mage_atkrange = 350

    def update(self):
        direction = atan_to_degree(self.change_x,self.change_y)
        self.direction = direction if direction != None else self.direction
        self.status = "in_motion" if direction != None else "idle"
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.left < 0:
            self.left = 0
        elif self.right > WIDTH:
            self.right = WIDTH
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > HEIGHT:
            self.top = HEIGHT

    def animation(self):
        self.step=(self.step+1)%20
        try:
            self.texture=self.dir_textures[self.direction,self.status][self.step//5]
        except KeyError:
            self.texture = self.textures[3]

class Monster(arcade.Sprite):
    class Health_bar(arcade.SpriteSolidColor):
            def __init__(self,length,thickness,color):
                super().__init__(length,thickness,color)

    def __init__(self,image,begin_x,begin_y,attack,defence,health,speed,scale=1):
        super().__init__(filename=image,scale=scale)
        self.center_x = begin_x
        self.center_y = begin_y
        self.attack = attack
        self.defence = defence
        self.maxhealth = health
        self.health = health
        self.speed = speed*60/FPS
        self.health_bar_length = int(self.width*3/4)
        self.health_bar_thickness = int(self.height/15)
        self.health_bar = self.Health_bar(self.health_bar_length,self.health_bar_thickness,arcade.color.ALABAMA_CRIMSON)

    def update(self):
        self.health_bar.width = self.health_bar_length*self.health/self.maxhealth
        self.health_bar.left = self.center_x - self.health_bar_length/2
        self.health_bar.bottom = self.top + 10

class NPC(arcade.Sprite):
    def __init__(self,filename,begin_x,begin_y,speed=1):
        super().__init__(filename=filename,scale=1)
        self.center_x = begin_x
        self.center_y = begin_y
        self.speed = speed*60/FPS
        self.count_update = 0
        self.direction = None

    def update(self):
        if self.count_update == 0:
            self.direction = random.choice(DIRECTIONS+["stay","stay","stay"])
        if self.direction == "up":
            self.change_y = self.speed
        elif self.direction == "down":
            self.change_y = -self.speed
        elif self.direction == "right":
            self.change_x = self.speed
        elif self.direction == "left":
            self.change_x = -self.speed
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.change_x = 0
        self.change_y = 0
        self.count_update += 1
        if self.count_update == FPS*2:
            self.count_update = 0

class Item(arcade.Sprite):
    def __init__(self,image,x,y):
        super().__init__(filename=image)
        self.center_x = x
        self.center_y = y

class Game(arcade.View):
    def __init__(self):
        super().__init__()
        self.sprite_list=None
        self.sound=None
        self.view_left=0
        self.setup()
        self.monster_be_hurt = []

    def setup(self):
        self.item_list = arcade.SpriteList()
        self.monster_list = arcade.SpriteList()
        self.npc_list = arcade.SpriteList()
        self.sprite_list = arcade.SpriteList()
        self.sword = Item("./image/npc.png",600,600)
        self.apple = Item("./image/npc.png",400,600)
        self.rabbit1 = Monster("./image/monster.png",600,700,10,2,20,10)
        self.rabbit2 = Monster("./image/monster.png",200,700,10,2,20,10)
        self.rabbit3 = Monster("./image/monster.png",600,800,10,2,20,10)
        self.dog = Monster("./image/dog.png",300,300,10,2,20,10)
        self.troy = NPC("./image/monster.png",500,400)
        self.teacher = NPC("./image/npc.png", 300,500)
        self.student = NPC("./image/npc.png", 300,600)
        self.player = Player(300,400,attack=4,defence=3,health=20,atkrange=150,speed=3)
        self.messagebox = ui.Message_box(self)
        self.optionbox = ui.Option_box(self)
        self.dialogue = ui.Dialogue_box(self)
        self.infobox = ui.Infobox()
        for item in [self.sword,self.apple]:
            self.item_list.append(item)
            self.sprite_list.append(item)
        for monster in [self.rabbit1,self.rabbit2,self.rabbit3,self.dog]:
            self.monster_list.append(monster)
            self.sprite_list.append(monster)
        for npc in [self.troy, self.teacher, self.student]:
            self.npc_list.append(npc)
            self.sprite_list.append(npc)
        self.sprite_list.append(self.player)
        #self.player.career set up
        self.bullet = arcade.Sprite("./image/bullet.png")
        self.fireball = arcade.Sprite("./image/bullet.png",scale=8)

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.background =  arcade.load_texture('./image/map.png',0,0,640,640,scale=1)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(WIDTH//2,HEIGHT//2,1280,1280,self.background)
        self.infobox.draw()
        super().on_draw()
        self.sprite_list.draw()

        for monster in self.monster_list:
            monster.health_bar.draw()

    def on_update(self,delta_time):
        changed=False
        right_bound=self.view_left+WIDTH*0.8
        if self.player.right > right_bound:
            self.view_left += self.player.right - right_bound
            self.dialogue.center_x += self.player.right - right_bound
            changed = True
        left_bound=self.view_left+WIDTH*0.2
        if self.player.left < left_bound:
            self.view_left -= left_bound - self.player.left 
            self.dialogue.center_x -= left_bound - self.player.left 
            changed = True
        if changed:
            arcade.set_viewport(self.view_left,self.view_left+WIDTH,0,HEIGHT)
        self.player.animation()
        self.sprite_list.update()

        if self.bullet in self.sprite_list:
            monsters = arcade.check_for_collision_with_list(self.bullet,self.monster_list)
            if monsters != []:
                for monster in monsters:
                    self.monster_be_hurt.append(monster)
                self.bullet.kill()
            if get_distance(self.bullet_resource_x,self.bullet_resource_y,self.bullet.center_x,self.bullet.center_y) >= self.player.gunner_atkrange:
                self.bullet.kill()
        if self.fireball in self.sprite_list:
            monsters = arcade.check_for_collision_with_list(self.fireball,self.monster_list)
            if monsters != []:
                for monster in monsters:
                    if monster not in self.monster_be_hurt_with_fireball:
                        self.monster_be_hurt.append(monster)
                        self.monster_be_hurt_with_fireball.append(monster)
            if get_distance(self.fireball_resource_x,self.fireball_resource_y,self.fireball.center_x,self.fireball.center_y) >= self.player.mage_atkrange:
                self.fireball.kill()
        for monster in self.monster_be_hurt:
            monster.health -= self.player.attack-monster.defence
            if monster.health < 0:
                monster.health = 0
        for monster in self.monster_list:
            if monster.health == 0:
                ｍonster.kill()
        """
        for index in TRANSPORT.keys():
            for sprite in self.sprite_list:
                if abs(sprite.center_x-index[0]) < 100 and abs(sprite.center_y-index[1]) < 100:
                    sprite.center_x,sprite.center_y = TRANSPORT[index]
        """
        self.monster_be_hurt = []

    def on_key_press(self,key,modifier):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        if key == arcade.key.W:
            self.player.change_y += self.player.speed
        elif key == arcade.key.S:
            self.player.change_y -= self.player.speed
        if key == arcade.key.D:
            self.player.change_x += self.player.speed
        elif key == arcade.key.A:
            self.player.change_x -= self.player.speed
        if key == arcade.key.SPACE:
            self.player_attack()
        if key == arcade.key.C:
            self.player_pick()
        if key==arcade.key.T: 
            if arcade.get_distance_between_sprites(self.player,self.teacher)<130:
                self.texture=arcade.Texture('texture',arcade.get_image())
                self.window.show_view(self.dialogue)
            if arcade.get_distance_between_sprites(self.player,self.dog)<130:
                self.texture=arcade.Texture('texture',arcade.get_image())
                self.window.show_view(self.optionbox)
            if arcade.get_distance_between_sprites(self.player,self.troy)<130:
                self.texture=arcade.Texture('texture',arcade.get_image())
                self.window.show_view(self.messagebox)

    def on_key_release(self,key,modifier):
        if key == arcade.key.W:
            self.player.change_y -= self.player.speed
        elif key == arcade.key.S:
            self.player.change_y += self.player.speed
        if key == arcade.key.D:
            self.player.change_x -= self.player.speed
        elif key == arcade.key.A:
            self.player.change_x += self.player.speed

    def player_attack(self):
        if self.player.career == None:
            monster_in_range = []
            for monster in self.monster_list:
                if arcade.get_distance_between_sprites(self.player,monster) <= self.player.atkrange :
                    monster_in_range.append(monster)
            for monster in monster_in_range:
                if not in_sector(monster.center_x,monster.center_y,self.player.center_x,self.player.center_y,self.player.direction):
                    monster_in_range.remove(monster)
            if monster_in_range != []:
                monster,distance = arcade.get_closest_sprite(self.player,monster_in_range)
                self.monster_be_hurt.append(monster)
        elif self.player.career == "gunner":
            if self.bullet not in self.sprite_list:
                self.bullet_resource_x , self.bullet_resource_y = self.player.center_x , self.player.center_y
                self.bullet.center_x , self.bullet.center_y = polar_coordinate_to_cartesian(self.player.direction,self.player.bullet_begin_distance_with_player,self.player.center_x,self.player.center_y)
                self.bullet.change_x , self.bullet.change_y = polar_coordinate_to_cartesian(self.player.direction,self.player.bullet_speed,0,0)
                self.sprite_list.append(self.bullet)
        elif self.player.career == "mage":
            if self.fireball not in self.sprite_list:
                self.monster_be_hurt_with_fireball = []
                self.fireball_resource_x , self.fireball_resource_y = self.player.center_x , self.player.center_y
                self.fireball.center_x , self.fireball.center_y = polar_coordinate_to_cartesian(self.player.direction,self.player.fireball_begin_distance_with_player,self.player.center_x,self.player.center_y)
                self.fireball.change_x , self.fireball.change_y = polar_coordinate_to_cartesian(self.player.direction,self.player.fireball_speed,0,0)
                self.sprite_list.append(self.fireball)

    def player_pick(self):
        item,distance = arcade.get_closest_sprite(self.player,self.item_list)
        if arcade.check_for_collision(self.player,item):
            self.player.possession.append(item)
            self.sprite_list.append(item)
            #item.kill()

class MyGame(arcade.Window):
    def __init__(self,width,height,title,color):
        super().__init__(width,height,title,fullscreen=True)
        super().set_update_rate(1/FPS)
        arcade.set_background_color(arcade.color.GRAY)
        game=Game()
        self.show_view(game) 

def main():
    game = MyGame(WIDTH,HEIGHT,TITLE,BACKGROUND_COLOR)
    #game.setup()
    arcade.run()

main()
