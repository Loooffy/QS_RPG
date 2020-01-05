import arcade
import random
import ui
from config import *

class Player(arcade.Sprite):
    def __init__(self,begin_x,begin_y,attack,defence,health,atkrange,speed):
        super().__init__()
        self.textures=arcade.load_spritesheet('./image/player_moves.png',96,96,4,16)
        self.step=0
        self.dir_textures={
            's':[self.textures[0],self.textures[1],self.textures[2],self.textures[3]],
            'e':[self.textures[4],self.textures[5],self.textures[6],self.textures[7]],
            'n':[self.textures[8],self.textures[9],self.textures[10],self.textures[11]],
            'w':[self.textures[12],self.textures[13],self.textures[14],self.textures[15]],
            'idle_s':[self.textures[3],self.textures[3],self.textures[3],self.textures[3]],
            'idle_e':[self.textures[7],self.textures[7],self.textures[7],self.textures[7]],
            'idle_n':[self.textures[11],self.textures[11],self.textures[11],self.textures[11]],
            'idle_w':[self.textures[15],self.textures[15],self.textures[15],self.textures[15]]
            }
        self.texture=self.dir_textures['idle_n'][0]
        self.direction='idle_s'
        self.center_x = begin_x
        self.center_y = begin_y
        self.attack = attack
        self.defence = defence
        self.maxhealth = health
        self.health = health
        self.atkrange = atkrange
        self.speed = speed*60/FPS
        self.change_x = 0
        self.change_y = 0
        self.possession = arcade.SpriteList()

    def update(self):
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
        self.texture=self.dir_textures[self.direction][self.step//5]

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
        self.speed = speed
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

    def setup(self):
        self.item_list = arcade.SpriteList()
        self.monster_list = arcade.SpriteList()
        self.npc_list = arcade.SpriteList()
        self.sprite_list = arcade.SpriteList()
        self.sword = Item("./image/pick.png",600,600)
        self.apple = Item("./image/pick.png",400,600)
        self.rabbit = Monster("./image/dog.png",600,700,10,2,20,10)
        self.troy = NPC("./image/pick.png",500,400)
        self.teacher = NPC("./image/npc.png", 300,500)
        self.student = NPC("./image/pick.png", 300,600)
        self.player = Player(300,400,attack=4,defence=3,health=20,atkrange=150,speed=3)
        self.dialogue = ui.Dialogue(self)
        self.infobox = ui.Infobox()
        for item in [self.sword,self.apple]:
            self.item_list.append(item)
            self.sprite_list.append(item)
        for monster in [self.rabbit]:
            self.monster_list.append(monster)
            self.sprite_list.append(monster)
        for npc in [self.troy, self.teacher, self.student]:
            self.npc_list.append(npc)
            self.sprite_list.append(npc)
        self.sprite_list.append(self.player)
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
        for monster in self.monster_list:
            if monster.health == 0:
                ｍonster.kill()
        for index in TRANSPORT.keys():
            for sprite in self.sprite_list:
                if abs(sprite.center_x-index[0]) < 100 and abs(sprite.center_y-index[1]) < 100:
                    sprite.center_x,sprite.center_y = TRANSPORT[index]

    def on_key_press(self,key,modifier):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        if key == arcade.key.W:
            self.player.direction='n'
            self.player.change_y += self.player.speed
        elif key == arcade.key.S:
            self.player.direction='s'
            self.player.change_y -= self.player.speed
        if key == arcade.key.D:
            self.player.direction='e'
            self.player.change_x += self.player.speed
        elif key == arcade.key.A:
            self.player.direction='w'
            self.player.change_x -= self.player.speed
        if key == arcade.key.SPACE:
            self.player_attack()
        if key == arcade.key.C:
            self.player_pick()
        if key==arcade.key.T and arcade.get_distance_between_sprites(self.player,self.teacher)<130:
            self.texture=arcade.Texture('texture',arcade.get_image())
            self.window.show_view(self.dialogue)

    def on_key_release(self,key,modifier):
        if key == arcade.key.W:
            self.player.change_y -= self.player.speed
            self.player.direction='idle_n'
        elif key == arcade.key.S:
            self.player.direction='idle_s'
            self.player.change_y += self.player.speed
        if key == arcade.key.D:
            self.player.direction='idle_e'
            self.player.change_x -= self.player.speed
        elif key == arcade.key.A:
            self.player.direction='idle_w'
            self.player.change_x += self.player.speed

    def player_attack(self):
        monster_hurt = []
        for monster in self.monster_list:
            if arcade.get_distance_between_sprites(self.player,monster) <= self.player.atkrange:
                monster_hurt.append(monster)
        for monster in monster_hurt:
            monster.health -= self.player.attack-monster.defence
            if monster.health < 0:
                monster.health = 0
    
    def player_pick(self):
        item,distance = arcade.get_closest_sprite(self.player,self.item_list)
        if arcade.check_for_collision(self.player,item):
            item.center_x+=1600
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
