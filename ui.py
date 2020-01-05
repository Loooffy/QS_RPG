import arcade
import utils
from config import *

class Infobox:
    def __init__(self):
        self.texture=arcade.load_texture('./image/infobox.png',0,0,300,900)
    
    def draw(self):
        arcade.draw_texture_rectangle(WIDTH-200,HEIGHT//2,300,900,self.texture)
        arcade.draw_text(utils.readtext(INFOBOX_TITLES),WIDTH-300,100,arcade.color.BLACK_LEATHER_JACKET,align="left",font_name='404notfont',font_size=20)

class Dialogue(arcade.View):
    def __init__(self,game_view):
        super().__init__()
        self.change_x=0
        self.game_view=game_view
        self.center_x=game_view.view_left+WIDTH//2
        self.words_per_line=16
        self.dialogue=utils.text_warp(utils.readtext('./text/dialogue.txt'),self.words_per_line)
        self.box_texture=arcade.load_texture('./image/dialogue_box.png',0,0,960,240)
        self.portrait_texture=arcade.load_texture('./image/pick.png',0,0,128,128)
        self.text_display=''
        self.line_num=0
        self.GRID=55

    def display_text(self, text):
        arcade.draw_texture_rectangle(self.center_x,130,960,240,self.box_texture)
        arcade.draw_texture_rectangle(self.center_x-350,130,128,128,self.portrait_texture)
        arcade.draw_text(self.text_display,WIDTH//2-200,70,color=WHITE,align="left",font_name='404notfont',font_size=20,spacing=self.GRID//2)

    def on_show(self):
            self.line_num=0
            self.text_display=''
            for i in range(0,3):
                self.text_display+=self.dialogue[self.line_num+i]
            self.line_num+=1

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(WIDTH//2,HEIGHT//2,WIDTH,HEIGHT,self.game_view.texture)
        if self.text_display not in ('','\n'):
            self.display_text(self.dialogue)

    def on_key_press(self,key,modifiers):
        if key==arcade.key.ESCAPE:
            self.window.show_view(self.game_view) 

        if key == arcade.key.SPACE and self.line_num+2<len(self.dialogue):
            self.text_display=''
            for i in range(0,3):
                self.text_display+=self.dialogue[self.line_num+i]
            self.line_num+=1

    def on_update(self,delta_time):
        self.center_x += self.change_x
