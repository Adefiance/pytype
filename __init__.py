"""
Simple typing and classes for pygame, to make life a tad bit easier.

This module added a few classes and some typing for you!
With this module, you can draw a rect or circle directly from the 'draw' property in a surface!, for example:
    ```python
    mySurf = pytype.Surface((50, 50))
    # pygame.draw.rect(mySurf, (255, 0, 0), (50, 50, 50, 50)) - This is a little longer.
    mySurf.draw.rect((255, 0, 0), (50, 50, 50, 50)) 
    ```
It's a very small change, but it helps!

However, with pytype.Surface, to support draw. There was a slight change. The actual surface has been placed in .getSurface(), so watch out!
    ```python
    print(mySurf.getSurface()) # Gives you the actual surface.
    ```
This also has a Display class, that allows you to also draw directly onto the display, aswell as resize the screen at your will!
    ```python
    myDisplay: pytype.Display = pytype.Display()
    myDisplay.resize((500, 500), (True, True)) 
    ```
It can also scale the contents from the x and y axis!

Genuinelly hope you like using this, Have fun!
"""

from pytype.classes import *
from pytype.simple import *

pygame = None
"""Try NOT accessing pygame from here! This WILL cause an error!"""
Literal = None
"""Not this either!!"""
typing = None
"""NO."""

del pygame, Literal, typing