"""
Simple typing file.

Holder for types like PolyValue and Coordinate, aswell as a few types that aren't necessarily pygame-related.
"""

from typing import Literal

# Not related to pygame.
type anyBool = bool | Literal[0, 1]
"""Allows for more leniency"""

#  More likely to show up
type ColorValue = tuple[int, int, int] | tuple[int, int, int, int]
"""This type accepts RGB(A) values only."""

type Coordinate = tuple[int, int]
"""Used for 2 dimensional sizing and positions"""

type RectValue = tuple[int, int, int, int] | tuple[tuple[int, int], tuple[int, int]]
"""Used to check for values compatible with pygame.Rect"""

type PolyValue = tuple[Coordinate, Coordinate, Coordinate, *tuple[Coordinate, ...]]
"""Used to check for values compatible with pygame.draw.polygon's "points" arguments"""
