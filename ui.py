import arcade
import config
import utils
from config import *

class Text_box(arcade.View):
    def __init__(self, center_x, center_y, width, height, text = '', color=None, texture='',previous_view=None,scale=1,change_x=0,change_y=0):
        super().__init__()
        self.center_x = center_x
        self.center_y = center_y
        self.change_x = 0
        self.change_y = 0
        self.width = width
        self.height = height
        self.text = text
        self.scale = scale
        self.color = color
        self.previous_view = previous_view
        self.texture = arcade.load_texture(texture,0,0,self.width,self.height)
            
    def return_to_map(self):
        self.window.show_view(self.previous_view) 

    def draw(self):
        if self.texture:
            arcade.draw_texture_rectangle(self.center_x+self.change_x,self.center_y+self.change_y,self.width*self.scale,self.height*self.scale,self.texture)
        if self.color:
            arcade.draw_rectangle_filled(self.center_x+self.change_x,self.center_y+self.change_y,self.width,self.height,self.color)
        if self.text != '':
            arcade.draw_text(self.text,self.center_x-self.width*self.scale//2+self.change_x+TEXT_MARGIN_H,self.center_y-self.height*self.scale//2+self.change_y+TEXT_MARGIN_V,WHITE,align="left",font_name='404notfont',font_size=20)
        else:
             pass

class Infobox(Text_box):
    def __init__(self,previous_view):
        self.items=arcade.SpriteList()
        text = utils.readtext(INFOBOX_TITLES)
        super().__init__(WIDTH-INFOBOX_WIDTH//2,HEIGHT//2,300,900,texture='./image/infobox.png',text=text)
        self.energy_texture=arcade.load_texture('./image/energy.png',0,0,64,64)
        self.previous_view=previous_view

    def add_item(self,item):
        self.items.append(item)
        item.center_x = WIDTH - INFOBOX_WIDTH//2 - 100
        item.center_x += len(self.items)*60
        item.center_y = 400
    
    def draw(self):
        super().draw()
        if len(self.items) != 0:
            self.items.draw()
        for i in range(0,self.previous_view.player.energy):
            arcade.draw_texture_rectangle(WIDTH-INFOBOX_WIDTH//2+self.change_x+32*i,HEIGHT//2+200,32,32,self.energy_texture)

class Dialogue_box(Text_box):
    def __init__(self, previous_view, dialogue, char_per_line=CHAR_PER_LINE, spacing=SPACING, portrait_A=None, portrait_B=None):
        super().__init__(DB_CENTER_X,DB_CENTER_Y,DB_WIDTH,DB_HEIGHT,texture='./image/dialogue_box.png', previous_view=previous_view)
        self.char_per_line = char_per_line
        self.dialogue = utils.text_wrap(utils.readtext(dialogue), self.char_per_line)
        self.portrait_A = arcade.load_texture(portrait_A,0,0,128,128)
        self.portrait_B = portrait_B
        self.text_display = ''
        self.line_num=0
        self.spacing = spacing
    
    def load_next_line(self,line_num):
        self.text_display=''
        for i in range(0,3):
            self.text_display+=self.dialogue[line_num+i]
        self.line_num+=1

    def display_text(self, text):
        arcade.draw_texture_rectangle(DB_P_X+self.change_x,DB_P_Y,DB_P_W,DB_P_H,self.portrait_A)
        arcade.draw_text(self.text_display,DB_T_X+self.change_x,DB_T_Y,color=WHITE,align="left",font_name='404notfont',font_size=20,spacing=self.spacing)

    def on_show(self):
        self.line_num=0
        self.load_next_line(self.line_num)
    
    def on_draw(self):
        super().draw()
        if self.text_display not in ('','\n'):
            self.display_text(self.dialogue)

    def on_key_press(self,key,modifiers):
        if key==arcade.key.ESCAPE:
            super().return_to_map()
        if key == arcade.key.SPACE:
            if self.line_num+2<len(self.dialogue):
                self.load_next_line(self.line_num)
            else:
                super().return_to_map()

class Message_box(Text_box):
    def __init__(self,previous_view,condition='get',icon=None):
        self.condition=condition
        self.previous_view=previous_view
        text=MSG_CONDITION[self.condition]
        super().__init__(MSG_BOX_X,MSG_BOX_Y,MSG_BOX_W,MSG_BOX_H,texture='./image/dialogue_box.png',text=text,previous_view=self.previous_view,scale=0.5)
        self.item_texture=arcade.load_texture('./image/pick.png',0,0,128,128)

    def set_condition(self,condition):
        self.condition=condition
        text=MSG_CONDITION[self.condition]
        super().__init__(MSG_BOX_X,MSG_BOX_Y,MSG_BOX_W,MSG_BOX_H,texture='./image/dialogue_box.png',text=text,previous_view=self.previous_view,scale=0.5)

    def on_draw(self):
        super().draw()
        arcade.draw_texture_rectangle(MSG_I_X+self.change_x,MSG_I_Y+self.change_y,MSG_I_W,MSG_I_H,self.item_texture)

    def on_key_press(self,key,modifiers):
        if key in [arcade.key.ESCAPE, arcade.key.SPACE]:
            self.return_to_map()

class Option_box(Text_box):
    def __init__(self,previous_view):
        text='是'+'　'*14+'否'
        texture='./image/dialogue_box.png'
        super().__init__(OPT_BOX_X,OPT_BOX_Y,OPT_BOX_W,OPT_BOX_H,texture=texture,text=text,previous_view=previous_view,scale=0.5)
        self.cursor_texture=arcade.load_texture('./image/pick.png',0,0,128,128,scale=1)
        self.cursor_move=0
        self.answer=True

    def on_draw(self):
        super().draw()
        arcade.draw_texture_rectangle(OPT_C_X+self.change_x+self.cursor_move,OPT_C_Y,OPT_C_W,OPT_C_H,self.cursor_texture)

    def on_key_press(self,key,modifiers):
        if key == arcade.key.D:
            if self.cursor_move == 0:
                self.cursor_move += OPT_C_MOVE
                self.answer= not self.answer
        if key == arcade.key.A:
            if self.cursor_move != 0:
                self.cursor_move -= OPT_C_MOVE
                self.answer= not self.answer
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.previous_view)
        if key in [arcade.key.ENTER, arcade.key.SPACE]:
            if self.answer == True:
                self.previous_view.player.energy-=1
                self.window.show_view(self.previous_view)
            else:
                self.window.show_view(self.previous_view)
