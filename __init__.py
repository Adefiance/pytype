"""
Simple typing and classes for pygame, to make life a tad bit easier.

This module added a few classes and some typing for you!
With this module, you can draw a rect or circle, for example, directly from the 'draw' property in a surface!, for example:
```python
from pytype import PSurface
mySurf = PSurface((50, 50))
# pygame.draw.rect(mySurf, (255, 0, 0), (50, 50, 50, 50)) - OR, you can use:
mySurf.draw.rect((255, 0, 0), (50, 50, 50, 50)) 
```
It's a very small change, but it helps!
This also has a Display class, that allows you to also draw directly onto the display, aswell as resize the screen at your will!
```python
myDisplay: pytype.Display = pytype.Display()
myDisplay.resize((500, 500), (True, True)) 
```
It can also scale the contents from the x and y axis!

Genuinelly hope you like using this, Have fun!
"""

from pytype.simple import AlphaValue, AnyBool, ColorValue, Coordinate, PolyValue, RectValue
from pytype.classes import PDisplay, PSurface, PRect
