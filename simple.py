from typing import Literal
from pygame import Rect

# Not related to pygame.
type AnyBool = bool | Literal[0, 1]
"""Allows for more leniency"""

#  Likely to show up
type ColorValue = tuple[int, int, int] | tuple[int, int, int, int]
"""Accepts RGB/A values only."""

type AlphaValue = tuple[int, int, int, int]
"""Accepts RGBA values only."""

type Coordinate = tuple[int, int] 
"""Used for 2 dimensional sizing and positions"""

type RectValue = tuple[int, int, int, int] | tuple[tuple[int, int], tuple[int, int]] | Rect
"""Used to check for values compatible with pygame.Rect"""

type PolyValue = tuple[Coordinate, Coordinate, Coordinate, *tuple[Coordinate, ...]]
"""Used to check for values compatible with pygame.draw.polygon's or lines/aalines' "points" arguments"""