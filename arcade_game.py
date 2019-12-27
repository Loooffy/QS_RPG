import arcade

SCREEN_WIDTH=800
SCREEN_HEIGHT=600
SCREEN_TITLE='hello world'

class Game(arcade.View):
    def __init__(self):
        super().__init__()
        self.man=None
        self.spritelist=None
        self.sound=None
        self.view_left=0
        self.box=None

    def setup(self):
        self.man=arcade.Sprite('walk1.png',1,center_x=200,center_y=150)
        self.spritelist=arcade.SpriteList()
        self.spritelist.append(self.man)
        self.sound=arcade.Sound('in.wav')

    def on_show(self):
        arcade.set_background_color(arcade.color.ASH_GREY)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_rectangle_filled(300,300,50,50,arcade.color.BLACK)
        self.spritelist.draw()
    
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
            print(self.view_left)
            arcade.set_viewport(self.view_left,self.view_left+SCREEN_WIDTH,0,SCREEN_HEIGHT)
        self.man.update()

    def on_key_press(self,key,modifiers):
        if key==arcade.key.W:
            self.man.change_y=5
        if key==arcade.key.S:
            self.man.change_y=-5
        if key==arcade.key.D:
            self.man.change_x=5
        if key==arcade.key.A:
            self.man.change_x=-5
        if key==arcade.key.I:
            self.texture=arcade.Texture('texture',arcade.get_image())
            inventory=Invetory(self)
            self.window.show_view(inventory)
            arcade.play_sound(self.sound)

    def on_key_release(self,key,modifiers):
        if key==arcade.key.W:
            self.man.change_y=0
        if key==arcade.key.S:
            self.man.change_y=0
        if key==arcade.key.D:
            self.man.change_x=0
        if key==arcade.key.A:
            self.man.change_x=0

class Invetory(arcade.View):
    def __init__(self,game_view):
        super().__init__()
        self.game_view=game_view
        self.points=[(325,90),(375,90),(425,90),(475,90)]

    def on_show(self):
        arcade.set_background_color(arcade.color.ASH_GREY)
    
    def on_draw(self):
        arcade.start_render()
        arcade.draw_rectangle_filled(400,100,220,100,arcade.color.ORANGE)
        arcade.draw_points(self.points,arcade.color.AFRICAN_VIOLET,45)
        arcade.draw_text('inventory',325,120,arcade.color.WHITE,font_size=18,width=175,align="center")
   
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
