import arcade

SCREEN_WIDTH=800
SCREEN_HEIGHT=600
SCREEN_TITLE='hello world'

class Man(arcade.Sprite):
    def __init__(self):
        super().__init__()
        walk1=arcade.load_texture('walk1.png')
        walk2=arcade.load_texture('walk2.png')
        walk3=arcade.load_texture('walk3.png')
        walk4=arcade.load_texture('walk4.png')
        walk5=arcade.load_texture('walk5.png')
        self.direction='idle'
        self.step=0
        self.images={'n':[walk1,walk2],'s':[walk1,walk2],'w':[walk3,walk4],'e':[walk3,walk4],'idle':[walk1,walk1]}
        self.texture=self.images['idle'][0]
    
    def update_animation(self):
        self.step=(self.step+1)%14
        self.texture=self.images[self.direction][self.step//7]

class Game(arcade.View):
    def __init__(self):
        super().__init__()
        self.man=None
        self.spritelist=None
        self.sound=None
        self.view_left=0
        self.box=None
        self.dialogue_box_list=[]

    def setup(self):
        self.man=Man()
        self.man._set_collision_radius(80)
        self.box=arcade.Sprite('box1.png',1,center_x=200,center_y=300)
        self.box_list=arcade.SpriteList()
        self.box_list.append(self.box)
        self.spritelist=arcade.SpriteList()
        self.spritelist.append(self.box)
        self.spritelist.append(self.man)
        self.physics_engine=arcade.PhysicsEngineSimple(self.man,self.box_list)
        self.sound=arcade.Sound('in.wav')
        self.add_dialogue_box()

    def add_dialogue_box(self):
        dialogue_box=arcade.gui.DialogueBox(200,100,500,100,arcade.color.OCHRE)
        message='hello'
        dialogue_box.text_list.append(arcade.gui.Text(message,150,150))
        self.dialogue_box_list.append(dialogue_box)
    
    def on_show(self):
        arcade.set_background_color(arcade.color.GRAY)

    def on_draw(self):
        arcade.start_render()
        self.spritelist.draw()
        super().on_draw()
    
    def on_update(self,delta_time):
        changed=False
        right_bound=self.view_left+SCREEN_WIDTH-128
        if self.man.right > right_bound:
            self.view_left += self.man.right - right_bound
            changed = True
        left_bound=self.view_left+SCREEN_WIDTH-672
        if self.man.left < left_bound:
            self.view_left -= left_bound - self.man.left 
            changed = True
        if changed:
            #print(self.view_left)
            arcade.set_viewport(self.view_left,self.view_left+SCREEN_WIDTH*3,0,SCREEN_HEIGHT*3)
        #print(self.man.direction,self.man.step,delta_time)
        self.man.update()
        self.man.update_animation()
        self.physics_engine.update()
        #print(self.man.get_points())

    def on_key_press(self,key,modifiers):
        if key==arcade.key.W:
            self.man.direction='n'
            self.man.change_y=5
        if key==arcade.key.S:
            self.man.direction='s'
            self.man.change_y=-5
        if key==arcade.key.D:
            self.man.direction='e'
            self.man.change_x=5
        if key==arcade.key.A:
            self.man.direction='w'
            self.man.change_x=-5
        if key==arcade.key.I:
            self.texture=arcade.Texture('texture',arcade.get_image())
            inventory=Invetory(self)
            self.window.show_view(inventory)
            arcade.play_sound(self.sound)
        if key==arcade.key.SPACE and arcade.get_distance_between_sprites(self.man,self.box)<130:
            self.dialogue_box_list[0].active=not self.dialogue_box_list[0].active

    def on_key_release(self,key,modifiers):
        if key==arcade.key.W:
            self.man.change_y=0
            self.man.direction='idle'
        if key==arcade.key.S:
            self.man.change_y=0
            self.man.direction='idle'
        if key==arcade.key.D:
            self.man.change_x=0
            self.man.direction='idle'
        if key==arcade.key.A:
            self.man.change_x=0
            self.man.direction='idle'

class Invetory(arcade.View):
    def __init__(self,game_view):
        super().__init__()
        self.game_view=game_view
        self.center_x=game_view.view_left+SCREEN_WIDTH//2
        self.points=[(self.center_x-100,60),(self.center_x-35,60),(self.center_x+35,60),(self.center_x+100,60)]

    def on_show(self):
        arcade.set_background_color(arcade.color.GRAY)
    
    def on_draw(self):
        arcade.start_render()
        arcade.draw_rectangle_filled(self.center_x,100,350,150,arcade.color.RED)
        arcade.draw_points(self.points,arcade.color.BLUE,45)
        arcade.draw_text('發大財',self.center_x-80,100,arcade.color.WHITE,width=175,align="center",font_name='404notfont',font_size=40)
   
    def on_key_press(self,key,modifiers):
        if key==arcade.key.ESCAPE:
            self.window.show_view(self.game_view) 

class Mygame(arcade.Window):
    def __init__(self,width,height,title,**kw):
        super().__init__(width,height,title,**kw)
        game=Game()
        game.setup()
        self.set_mouse_visible(False)
        self.show_view(game)

mygame=Mygame(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
arcade.run()
