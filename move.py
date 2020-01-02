import arcade
import random

SIZE = WIDTH , HEIGHT = 1440,900
TITLE = "Hi arcade"
BACKGROUND_COLOR = arcade.color.WHITE
FPS = 60

DIRECTIONS = ["up","right","down","left"]
TRANSPORT = {(720,450):(450,720)}

class Player(arcade.Sprite):
    def __init__(self,begin_x,begin_y,attack,defence,health,atkrange,speed):
        filename = "./monster.gif"
        super().__init__(filename=filename,scale=3)
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
class Monster(arcade.Sprite):
    class Health_bar(arcade.SpriteSolidColor):
            def __init__(self,length,thickness,color):
                super().__init__(length,thickness,color)
    def __init__(self,image,begin_x,begin_y,attack,defence,health,speed,scale=2):
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
    def __init__(self,image,begin_x,begin_y,speed=0.6):
        super().__init__(filename=image,scale=2)
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
class MyGame(arcade.Window):
    def __init__(self,width,height,title,color):
        super().__init__(width,height,title,fullscreen=True)
        super().set_update_rate(1/FPS)
        arcade.set_background_color(color)
    def setup(self):
        self.item_list = arcade.SpriteList()
        self.monster_list = arcade.SpriteList()
        self.npc_list = arcade.SpriteList()
        self.sprite_list = arcade.SpriteList()
        self.sword = Item("./image.gif",600,600)
        self.apple = Item("./image.gif",400,600)
        self.rabbit = Monster("./monster.gif",720,450,attack=3,defence=3,health=10,speed=0.5)
        self.troy = NPC("./monster.gif",500,400)
        self.player = Player(300,400,attack=4,defence=3,health=20,atkrange=150,speed=3)
        for item in [self.sword,self.apple]:
            self.item_list.append(item)
            self.sprite_list.append(item)
        for monster in [self.rabbit]:
            self.monster_list.append(monster)
            self.sprite_list.append(monster)
        for npc in [self.troy]:
            self.npc_list.append(npc)
            self.sprite_list.append(npc)
        self.sprite_list.append(self.player)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player,self.monster_list)
    def on_draw(self):
        arcade.start_render()
        self.sprite_list.draw()
        for monster in self.monster_list:
            monster.health_bar.draw()
    def on_update(self,delta_time):
        #super().set_viewport(self.player.left-288,self.player.right+288,self.player.bottom-180,self.player.top+180)
        self.sprite_list.update()
        for monster in self.monster_list:
            if monster.health == 0:
                ｍonster.kill()
        for index in TRANSPORT.keys():
            for sprite in self.sprite_list:
                if abs(sprite.center_x-index[0]) < 30 and abs(sprite.center_y-index[1]) < 30:
                    sprite.center_x,sprite.center_y = TRANSPORT[index]
        self.physics_engine.update()
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
            self.player.possession.append(item)
            item.kill()

def main():
    game = MyGame(WIDTH,HEIGHT,TITLE,BACKGROUND_COLOR)
    game.setup()
    arcade.run()
main()