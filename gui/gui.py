import pygame as pg
from enum import IntFlag
from dataclasses import dataclass

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
        if self.state & ElemState.PRESSED:
            self.state &= ~ElemState.PRESSED
        else:
            self.state |= ElemState.RAISED


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
            if event.type == pg.MOUSEBUTTONDOWN:
                self.state &= ElemState.PRESSED
                self.state &= ~ElemState.HOVER

            elif event.type == pg.MOUSEBUTTONUP:
                # only counts as a click if the elem
                # was previously pressed
                if self.state & ElemState.PRESSED:
                    self.flip_state()   # back to released 
                    self.onclick()
                    if self.callback:
                        self.callback(*self.callback_args)
        else:
            # to cancel an action, simply move the cursor
            # out of the bounding box to safely clear
            # the pressed state
            self.state &= ~ElemState.PRESSED
            self.state &= ~ElemState.HOVER

class  ElemState(IntFlag):
    """
    If PRESSED isn't present in a flag bitset,
    it means the element is raised
    """
    PRESSED = 0x1       
    HOVER = 0x2 


@dataclass
class GUIStyle:
    bg_color = (148, 17, 255)
    fg_color = (255, 255, 255)
    font = None             # string - font filename. (pg.font.get_default_font())
    border_color = None     # use a tuple to specify color
    border_thickness = None # use an integer



class Button(GUIElem):
    def __init__(self, screen, pos, width, height):
        super().__init__(screen, pos, width, height)
        self.state = 0          # state flags
       

    def draw(self):
        pg.draw.rect(self.screen, self.style.bg_color, self.rect)

        
class TextButton:
    def __init__(self, screen, pos, width, height, text):
        super().__init__(screen, pos, width, height)
        self.text = text

    def set_font(self, font):
        self.font = font

    def draw(self):
        super().draw()
        # render text 

class ImageButton(Button):
    def __init__(self, screen, pos, width, height, image):
        super().__init__(screen, pos, width, height)
        self.image = image


class GUI:

    def __init__(self, screen):
        self.screen = screen
        self.elems = []

    def add_button(self, pos, width, height, callback, callback_args):
        self.elems.append(
            Button(self.screen, pos, width, height)
             .set_callback(callback, callback_args))

    def add_text_button(self, pos, width, height, text, callback, callback_args):
        self.elems.append(
            TextButton(self.screen, pos, width, height, text)
             .set_callback(callback, callback_args))

    def update(self, event, mouse_pos):
        for elem in self.elems:
            elem.update(event, mouse_pos)

    def draw(self):
        for elem in self.elems:
            elem.draw()

