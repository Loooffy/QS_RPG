import arcade
import random

# TODO fit sreens with different resolution.
SIZE = WIDTH , HEIGHT = 1440,900
TITLE = "Hi arcade"
BACKGROUND_COLOR = arcade.color.WHITE
FPS = 30

DIRECTIONS = ["up","right","down","left"]
TRANSPORT = {(720,450):(450,720)}

class Player(arcade.Sprite):
    def __init__(self,begin_x,begin_y,attack,defence,health,atkrange,speed):
        filename = "./monster.png"
        super().__init__(filename=filename,scale=1.0)
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
            
class Health_bar(arcade.SpriteSolidColor):
            def __init__(self,width,height,color):
                super().__init__(width,height,color)

class Monster(arcade.Sprite):
    def __init__(self,begin_x,begin_y,attack,defence,health,speed,scale=1):
        filename = "./monster.png"
        super().__init__(filename=filename,scale=scale)
        self.center_x = begin_x
        self.center_y = begin_y
        self.attack = attack
        self.defence = defence
        self.maxhealth = health
        self.health = health
        self.speed = speed
        #self.set_health_bar()
        self.health_bar = Health_bar(int(self.width/2),int(self.height/15),arcade.color.RED_BROWN)

    def set_health_bar(self):
        self.health_bar = arcade.ShapeElementList()
        white_bar = arcade.create_rectangle_filled(self.center_x-self.width/2,self.top+10,self.width*7/8,self.height/8,arcade.color.WHITE)
        red_bar = arcade.create_rectangle_filled(self.center_x-self.width/2,self.top+10,self.width*7/8*self.health/self.maxhealth,self.height/8,arcade.color.RED)
        black_frame = arcade.create_rectangle_outline(self.center_x-self.width/2,self.top+10,self.width*7/8,self.height/8,arcade.color.BLACK,2)
        self.health_bar.append(white_bar)
        self.health_bar.append(red_bar)
        self.health_bar.append(black_frame)
    def update(self):
        pass

class NPC(arcade.Sprite):
    def __init__(self,begin_x,begin_y,speed=1):
        filename = "./monster.png"
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

class Invetory(arcade.View):
    def __init__(self,game_view):
        super().__init__()
        self.game_view=game_view
        self.center_x=game_view.view_left+WIDTH//2
        self.points=[(self.center_x-100,60),(self.center_x-35,60),(self.center_x+35,60),(self.center_x+100,60)]
        self.dialogue_box_list=[]

    def setup(self):
        self.add_dialogue_box()
        self.dialogue_box_list[0].active=True

    def add_dialogue_box(self):
        dialogue_box=arcade.gui.DialogueBox(WIDTH//2,300,WIDTH//2,100,arcade.color.BLACK)
        message1='hello, this is the first game we made in QS, hope it would be fun'
        message2='oh, yes, we have a game'
        dialogue_box.text_list.append(arcade.gui.Text(message1,WIDTH//2,300,color=arcade.color.WHITE,font_size=36,font_name='404notfont',bold=True))
        dialogue_box.text_list.append(arcade.gui.Text(message2,WIDTH//2,264,color=arcade.color.WHITE,font_size=36,font_name='404notfont',bold=True))
        self.dialogue_box_list.append(dialogue_box)
    
    def on_key_press(self,key,modifiers):
        if key==arcade.key.T:
            self.window.show_view(self.game_view) 
        '''
        if key==arcade.key.SPACE:
            self.dialogue_box_list[0].active=not self.dialogue_box_list[0].active
        '''

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
        self.sound=arcade.Sound('in.wav')
        self.sword = Item("./image.gif",600,600)
        self.apple = Item("./image.gif",400,600)
        self.rabbit = Monster(720,450,attack=3,defence=3,health=10,speed=0.5)
        self.troy = NPC(500,400)
        self.player = Player(300,400,attack=4,defence=3,health=20,atkrange=150,speed=3)
        self.sprite_list.append(self.player)
        for item in [self.sword,self.apple]:
            self.item_list.append(item)
            self.sprite_list.append(item)
        for monster in [self.rabbit]:
            self.monster_list.append(monster)
            self.sprite_list.append(monster)
        for npc in [self.troy]:
            self.npc_list.append(npc)
            self.sprite_list.append(npc)

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_rectangle_outline(WIDTH-303,HEIGHT//2+3,600,HEIGHT-6,arcade.color.BROWN,border_width=8)
        arcade.draw_text('發大財',WIDTH-450,HEIGHT//2,arcade.color.BROWN,align="center",font_name='404notfont',font_size=80)
        super().on_draw()
        self.sprite_list.draw()

    def on_update(self,delta_time):
        #super().set_viewport(self.player.left-288,self.player.right+288,self.player.bottom-180,self.player.top+180)
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
        if key==arcade.key.T and arcade.get_distance_between_sprites(self.player,self.apple)<130:
            self.texture=arcade.Texture('texture',arcade.get_image())
            inventory=Invetory(self)
            inventory.setup()
            self.window.show_view(inventory)

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
            item.center_x+=1600
            self.player.possession.append(item)
            self.sprite_list.append(item)
            #item.kill()

class MyGame(arcade.Window):
    def __init__(self,width,height,title,color):
        super().__init__(width,height,title,fullscreen=True)
        super().set_update_rate(1/FPS)
        #arcade.set_background_color(color)
        game=Game()
        self.show_view(game) 

def main():
    game = MyGame(WIDTH,HEIGHT,TITLE,BACKGROUND_COLOR)
    #game.setup()
    arcade.run()
main()
