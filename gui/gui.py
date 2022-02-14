from utils.bitset import BitSet
import pygame as pg
from enum import IntFlag
from dataclasses import dataclass

RATIO = 1       # rect height to font size ratio


class GUIElem:
    def __init__(self, screen, pos, width, height):
        """
        Properties:
            callback: ref to function object
        """
        self.screen = screen
        self.pos = pos
        self.width = width
        self.height = height
        self.style = GUIStyle()
        self.callback = None        # a hook for the programmer
        self.callback_args = []     # tuple of references
        self.state = BitSet()

        self.rect = pg.rect.Rect(self.pos[0], self.pos[1], width, height)

    def set_callback(self, func, args_tuple):
        """
        Returns self; for method chaining
        """
        self.callback = func
        self.callback_args = args_tuple
        return self     
    
    def set_style(self, style):
        """
        style: an object of type GUIStyle
        """
        self.style = style
    
    def flip_state(self):
        self.state.flip(ElemState.PRESSED)


    def onclick():
        """<to be overridden>"""
        pass

    def draw():
        """<to be overridden>"""
        pass

    def update(self, event, mouse_pos):
        """
        The base class only 
        """
        if self.rect.collidepoint(mouse_pos):
            self.state.set(ElemState.HOVER)

            if event.type == pg.MOUSEBUTTONDOWN:
                if not self.state.test(ElemState.PRESSED):
                    self.state.set(ElemState.PRESSED)

            elif event.type == pg.MOUSEBUTTONUP:
                # only counts as a click if the elem
                # was previously pressed
                if self.state.test(ElemState.PRESSED):
                    self.state.clear(ElemState.PRESSED)
                    self.onclick()
                    if self.callback:
                        self.callback(*self.callback_args)
        else:
            # to cancel an action, simply move the cursor
            # out of the bounding box to safely clear
            # the pressed state
            self.state.clear(ElemState.PRESSED)
            self.state.clear(ElemState.HOVER)

class  ElemState(IntFlag):
    """
    If PRESSED isn't present in a flag bitset,
    it means the element is raised
    """
    NONE = 0x0 
    PRESSED = 0x1       
    HOVER = 0x2 
    

class Color:
    def __init__(self, r=148, g=255, b=147):
        self.r = r
        self.g = g
        self.b = b
        self.raw = (self.r, self.g, self.b)

    def __repr__(self):
        #return f"<Color>({self.r},{self.g},{self.b})</Color>"
        return f"Color<#{hex(self.r)[2:]}{hex(self.g)[2:]}{hex(self.b)[2:]}>"


    @classmethod
    def new_lightened(cls, color):

        def lighten_color(c):
            return int( min(c * 1.2, 255) )

        r, g, b = list(map(lighten_color, (color.r, color.g, color.b)))
        return cls(r, g, b) 




@dataclass
class GUIStyle:
    bg_color = Color()
    bg_hover_color = Color.new_lightened(bg_color)
    fg_color = Color(255, 255, 255)
    
    font = 'Envy Code R Regular'    # string - system font name
    font_size = None                # None means auto (acc. to width)
    font_color = fg_color
    font_bold = False
    font_italic = False

    border_color = None             # use a tuple to specify color
    border_width = None             # use an integer (border thickness)

    def set_border(self, b_col, b_width):
        self.border_color = Color(b_col[0], b_col[1], b_col[2])
        self.border_width = b_width



class Button(GUIElem):
    def __init__(self, screen, pos, width, height):
        super().__init__(screen, pos, width, height)
       

    def draw(self):
        color = self.style.bg_color
        if self.state.test(ElemState.HOVER):
            color = self.style.bg_hover_color
        
        pg.draw.rect(self.screen, color.raw, self.rect)

        # draw border
        if self.style.border_width != 0:
            pg.draw.rect(self.screen, self.style.border_color.raw,
                    self.rect, self.style.border_width)

        
class TextButton(Button):
    def __init__(self, screen, pos, width, height, text):
        super().__init__(screen, pos, width, height)
        self.text = text
        self.font = self.make_pygame_font()
    
    def set_font(self, font_name, font_bold, font_italic):
        self.style.font = font_name
        self.style.font_bold = font_bold
        self.style.font_italic = font_italic
        self.font = self.make_pygame_font()

    def make_pygame_font(self):
        self.style.font_size = int(RATIO * self.rect.height)
        return pg.font.SysFont(self.style.font,
                        self.style.font_size,
                        self.style.font_bold,
                        self.style.font_italic)
        

    def draw(self):
        super().draw()
        text_surface = self.font.render(self.text, False, self.style.font_color.raw)

        # center the text
        textpos_x = self.pos[0] + (self.rect.width - text_surface.get_rect().width)/2
        textpos_y = self.pos[1] + (self.rect.height - text_surface.get_rect().height)/2
        
        self.screen.blit(text_surface, (textpos_x, textpos_y))

class ImageButton(Button):
    def __init__(self, screen, pos, width, height, image):
        super().__init__(screen, pos, width, height)
        self.image = image


### Dialog boxes
class DialogBox(GUIElem):
    def __init__(self, screen, pos, width, height):
        super().__init__(screen, pos, width, height)
        self.ok_button = None


class GUI:

    def __init__(self, screen):
        self.screen = screen
        self.elems = []

    def add_button(self, pos, width, height, callback, callback_args):
        self.elems.append(
            Button(self.screen, pos, width, height)
             .set_callback(callback, callback_args))
        return self.elems[-1]

    def add_text_button(self, pos, width, height, text, callback, callback_args):
        self.elems.append(
            TextButton(self.screen, pos, width, height, text)
             .set_callback(callback, callback_args))
        
        return self.elems[-1]

    def update(self, event, mouse_pos):
        for elem in self.elems:
            elem.update(event, mouse_pos)

    def draw(self):
        for elem in self.elems:
            elem.draw()

