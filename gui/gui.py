from utils.bitset import BitSet
import const
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

    def set_pos(self, pos):
        self.pos = pos
        self.rect.x, self.rect.y = pos

    def set_callback(self, func, args_tuple):
        """
        Returns self; for method chaining
        NOTE: if there is only one arg, make sure to write the
              tuple like so : (x,) [otherwise, it's just evaluated
              as an expression]
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


    def onclick(self):
        """<to be overridden>"""
        pass

    def draw(self):
        """<to be overridden>"""
        pass

    def update(self, event, mouse_pos):
        """
        The base class only 
        """
        if self.rect.collidepoint(mouse_pos):
            self.state.set(ElemState.HOVER)
                
            if event.type == pg.MOUSEBUTTONDOWN:
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

class ElemState(IntFlag):
    """
    If PRESSED isn't present in a flag bitset,
    it means the element is raised
    """
    NONE = 0x0 
    PRESSED = 0x1       
    HOVER = 0x2 

# for containers
class Orientation(IntFlag):
    NULL = 0x0
    HORIZONTAL = 0x1
    VERTICAL = 0x2
    

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
    def new_scaled(cls, scale, color):

        def scale_color(c):
            return int( min(c * scale, 255) )

        r, g, b = list(map(scale_color, (color.r, color.g, color.b)))
        return cls(r, g, b) 


@dataclass
class GUIStyle:
    bg_color = Color(222, 222, 222)
    bg_hover_color = None           # overrides default lightened color if set
    fg_color = Color(255, 255, 255)
    
    font = 'Envy Code R Regular'    # string - system font name
    font_size = None                # None means auto (acc. to width)
    font_color = Color(0, 0, 0)
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
            color = Color.new_scaled(1.2, color)
        # darkened color
        if self.state.test(ElemState.PRESSED):
            color = Color.new_scaled(0.8, color)
        
        pg.draw.rect(self.screen, color.raw, self.rect)

        # draw border
        if self.style.border_width:
            pg.draw.rect(self.screen, self.style.border_color.raw,
                    self.rect, self.style.border_width)

        
class TextButton(Button):
    def __init__(self, screen, pos, width, height, text):
        super().__init__(screen, pos, width, height)
        self.text = text
        self.font = self.make_pygame_font()
    
    def set_font(self, font_name, font_bold=False, font_italic=False):
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
        textpos_x = int( self.pos[0] + (self.rect.width - text_surface.get_rect().width)/2 )
        textpos_y = int( self.pos[1] + (self.rect.height - text_surface.get_rect().height)/2 )

        
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


### Containers
class Container(GUIElem):
    def __init__(self, screen, pos, width, height):
        super().__init__(screen, pos, width, height)
        self.items = []
        self.orientation = Orientation.HORIZONTAL
        self.direction = 1      # 1 for left-to-right, up-to-down. -1 for the opposite
        self.gap = 20
        self.margin = (20, 0)

    def set_orientation(self, ori):
        self.orientation = ori
        return self

    def push_items(self, *items):
        for item in items:
            self.push_item(item)

    def push_item(self, item):
        if self.items:
            last_item = self.items[-1]
            if self.orientation == Orientation.HORIZONTAL:
                new_x = last_item.pos[0] + (self.direction) * (last_item.width + self.gap)
                item.set_pos((new_x, last_item.pos[1]))
            else:
                new_y = last_item.pos[1] + (self.direction) * (last_item.height + self.gap)
                item.set_pos((last_item.pos[0], new_y))
        else:
            item.set_pos(self.pos)
            if self.direction == -1:
                if self.orientation == Orientation.HORIZONTAL:
                    pos = self.pos[0] - item.width, self.pos[1]
                else:
                    pos = self.pos[0], self.pos[1] - item.height

        self.items.append(item)

    def pop_item(self):
        return self.items.pop()

    def update(self, event, mouse_pos):
        for item in self.items:
            item.update(event, mouse_pos)

    def draw(self):
        for item in self.items:
            item.draw()

        if const.DEBUG_DRAW:
            rect = pg.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
            if self.direction == -1:
                if self.orientation == Orientation.HORIZONTAL:
                    rect.x -= rect.width
                else:
                    rect.y -= rect.height

            pg.draw.rect(self.screen, (0, 0, 255), rect, 2)

    

class GUI:

    def __init__(self, screen):
        self.screen = screen
        self.elems = []

    def add_elem(self, elem):
        self.elems.append(elem)

    def make_horizontal_container(self, pos, width, height):
        return (Container(self.screen, pos, width, height)
                .set_orientation(Orientation.HORIZONTAL))
    
    def make_vertical_container(self, pos, width, height):
        return (Container(self.screen, pos, width, height)
                .set_orientation(Orientation.VERTICAL))

    def make_button(self, pos, width, height, callback, callback_args):
        return (Button(self.screen, pos, width, height)
                .set_callback(callback, callback_args))

    def make_text_button(self, pos, width, height, text, callback, callback_args):
        return (TextButton(self.screen, pos, width, height, text)
                .set_callback(callback, callback_args))
        
    def update(self, event, mouse_pos):
        for elem in self.elems:
            elem.update(event, mouse_pos)

    def draw(self):
        for elem in self.elems:
            elem.draw()

