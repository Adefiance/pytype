"""
Classes used in pytype.
"""

from pytype.simple import ColorValue, RectValue, PolyValue, Coordinate, anyBool, AlphaValue
import typing
import pygame

class DrawWrapper:
    """
    The draw wrapper. This is what enables Surface and Display to be drawn on from the variable itself.

    Example:
    ```python
    mySurf: pytype.Surface = pytype.Surface((50, 50))s
    mySurf.draw.rect((255, 0, 0), (0, 0, 50, 50))
    ```
    This draws a simple rect onto mySurf.
    """
    def __init__(self, surface: pygame.surface.Surface): self.surface = surface
    def rect(self, color: ColorValue, rect: RectValue, width: int = 0): return pygame.draw.rect(self.surface, color, rect, width)
    def polygon(self, color: ColorValue, points: PolyValue, width: int = 0): return pygame.draw.polygon(self.surface, color, points, width)
    def circle(self, color: ColorValue, center: Coordinate, radius: int, width: int = 0): return pygame.draw.circle(self.surface, color, center, radius, width)
    def ellipse(self, color: ColorValue, rect: RectValue, width: int = 0): return pygame.draw.ellipse(self.surface, color, rect, width)
    def arc(self, color: ColorValue, rect: RectValue, start_angle: int, stop_angle: int, width: int = 1): return pygame.draw.arc(self.surface, color, rect, start_angle, stop_angle, width)
    def line(self, color: ColorValue, start: Coordinate, end: Coordinate, width: int = 1): return pygame.draw.line(self.surface, color, start, end, width)
    def lines(self, color: ColorValue, closed: anyBool, points: PolyValue, width: int = 1): return pygame.draw.lines(self.surface, color, bool(closed), points, width)
    def aaline(self, color, start: Coordinate, end: Coordinate, blend: int = 1): return pygame.draw.aaline(self.surface, color, start, end, blend)
    def aalines(self, color, closed: anyBool, points: PolyValue, blend: int = 1): return pygame.draw.aalines(self.surface, color, bool(closed), points, blend)
class Surface:
    """
    A Pytype Surface. Adds a few actions straight to the surface itself, including the main transformations and draw.
    
    Example:
    ```python
    mySurf: pytype.Surface = pytype.Surface((50, 50))
    mySurf.scaleBy(2) 
    ```
    This will return a Surface with both width and height multiplied by 2.

    Or, you can check the alpha values of the surface.

    Example:
    ```python
    if not mySurf.isAlpha(): 
        mySurf.setAlpha(85)
        print(mySurf.getAlpha())
    else:
        mySurf.convertAlpha()
        print(mySurf.getAlpha())
    ```
    """
    def __init__(self, size: Coordinate, flags: int = 0, depth: int = 0, masks: ColorValue | None = None):
        if depth != 0:
            if masks is None: raise ValueError("If you specify a nonzero depth, you must also specify masks")
            self._surf = pygame.Surface(size, flags, depth, masks)
        else: self._surf = pygame.Surface(size, flags)
        self.draw = DrawWrapper(self._surf)
    def scaleBy(self, size: int) -> None: self._surf = pygame.transform.smoothscale(self._surf, (self._surf.get_size()[0] * size, self._surf.get_size()[1] * size))
    def smooothscale(self, size: Coordinate) -> None: self._surf = pygame.transform.smoothscale(self._surf, size)
    def scale(self, size: Coordinate) -> None: self._surf = pygame.transform.scale(self._surf, size)
    def rotate(self, degree: int) -> None: self._surf = pygame.transform.rotate(pygame.transform.smoothscale(self._surf, self._surf.get_size()), degree)
    def flip(self, x: anyBool = False, y: anyBool = False) -> None: self._surf = pygame.transform.flip(self._surf, x, y)
    def isAlpha(self) -> bool: return self._surf.get_alpha() != None
    def getAlpha(self) -> int | None: return self._surf.get_alpha()
    def convertAlpha(self) -> None: self._surf = self._surf.convert_alpha()
    def setAlpha(self, value: int, flags: int = 0) -> None: return self._surf.set_alpha(value, flags)
    def getSurface(self) -> pygame.surface.Surface: return self._surf
    def blit(self, source: pygame.surface.Surface, dest: Coordinate | RectValue, area: RectValue | None = None, flags: int = 0) -> pygame.Rect: return self._surf.blit(source, dest, area, flags)
    def blits(self, sequence: typing.Sequence[ typing.Union[ typing.Tuple[pygame.surface.Surface, typing.Union[Coordinate, RectValue]], typing.Tuple[pygame.surface.Surface, typing.Union[Coordinate, RectValue], typing.Union[RectValue, int]], typing.Tuple[pygame.surface.Surface, typing.Union[Coordinate, RectValue], RectValue, int] ] ], doreturn: anyBool = 1) -> list[pygame.Rect] | None: return self._surf.blits(sequence, doreturn)   
class Rect (pygame.Rect):
    """
    This is (mostly) a normal Pygame Rect. 
    
    You can now get a pytype Surface or a TRUE pygame Surface through a single method

    Example:
    ```python
    myRect: pytype.Rect = pytype.Rect((50, 50), (50, 50))
    mySurf: pytype.Surface = myRect.onSurface((255, 0, 0))
    myTrueSurf: pygame.Surface = myRect.onTrueSurface((255, 0, 0))
    ```
    mySurf - a pytype Surface, coming with a draw property. Recommended.

    myTrueSurf - a normal, pygame Surface. Simple as that.
    """
    def onSurface(self: pygame.Rect, color: ColorValue, flags: int = 0, depth: int = 32, masks: AlphaValue | None = None, width: int = 0) -> Surface:
        """
        The onSurface method will return the Rect on a pytype Surface of its size.

        args: 
            `color` (Required) - The color of the returned Surface.
            `flags` - Flags that you want to set on the surface e.g pygame.SRCALPHA
            `depth` - The bit depth of the surface. Defaults to 32 bits
            `masks` - Defines how color channels are stored.
            `width` - Defines the size of the outline, if a non-zero integer is given rect will not be filled.
        """
        surface: Surface = Surface(self.size, flags, depth, masks)
        surface.draw.rect(color, pygame.Rect((0, 0), self.size), width)
        return surface
    def onTrueSurface(self: pygame.Rect, color: ColorValue, flags: int = 0, depth: int = 0, masks: AlphaValue | None = None, width: int = 0) -> pygame.Surface:
        """
        The onTrueSurface method will return the Rect on a normal pygame Surface of its size.

        args: 
            `color` (Required) - The color of the returned Surface.
            `flags` - Flags that you want to set on the surface e.g pygame.SRCALPHA
            `depth` - The bit depth of the surface. Defaults to 32 bits
            `masks` - Defines how color channels are stored.
            `width` - Defines the size of the outline, if a non-zero integer is given rect will not be filled.
        """
        if masks is not None: surface = pygame.Surface(self.size, flags, depth, masks)
        else: surface = pygame.Surface(self.size, flags, 32)
        pygame.draw.rect(surface, color, pygame.Rect((0, 0), self.size), width)
        return surface
class Display:
    """Display is mostly similiar to Surface. This will instead create a **window**, however."""
    def __init__(self, size: Coordinate = (0, 0), flags: int = 0, depth: int = 0, display: int = 0, vsync: int = 0):
        self._display = pygame.display.set_mode(size, flags, depth, display, vsync)
        self.draw = DrawWrapper(self._display)
        self._index = display
        self._vsync = vsync
    def getDisplay(self) -> pygame.Surface: """Returns the actual window itself: the real pygame Surface."""; return self._display
    def quit(self) -> None: """Kills the window instance."""; return pygame.display.quit()
    def blit(self, source: pygame.Surface, dest: Coordinate | RectValue, area: RectValue | None = None, flags: int = 0) -> pygame.Rect: return self._display.blit(source, dest, area, flags)
    def blits(self, sequence: typing.Sequence[ typing.Union[ typing.Tuple[pygame.Surface, typing.Union[Coordinate, RectValue]], typing.Tuple[pygame.Surface, typing.Union[Coordinate, RectValue], typing.Union[RectValue, int]], typing.Tuple[pygame.Surface, typing.Union[Coordinate, RectValue], RectValue, int] ] ], doreturn: anyBool = 1) -> list[pygame.Rect] | None: return self._display.blits(sequence, doreturn)
    def resize(self, size: Coordinate, scale: tuple[anyBool, anyBool] = (False, False)) -> None:
        """
        Allows you to resize and scale the display window freely.

        args:
            `size` - This is a tuple of two integers, that will decide how much to scale the window.
            `scaled` - This is also a tuple, now of two booleans, deciding which axis to scale.

        Example:
        ```python
        myScreen: pytype.Display = pytype.Display()
        myScreen.draw.rect((255, 0, 0), ((50, 50), (50, 50)))
        myScreen.resize((500, 500), (True, False))
        ```
        This will first initilaise a display window that covers the screen.
        It will then draw a rect object onto it and scale it to 500 by 500 pixels, and scale it ONLY by the x axis.
        """
        old = self._display.copy()
        new = pygame.display.set_mode(size, self.getDisplay().get_flags(), self.getDisplay().get_bitsize(), self._index, self._vsync)

        self._display = new
        self.draw = DrawWrapper(new)

        scaled = pygame.transform.scale(old, (new.get_size()[0] if scale[0] else old.get_size()[0], new.get_size()[1] if scale[1] else old.get_size()[1]))
        self.blit(scaled, (0, 0))
    def scroll(self, dx: int = 0, dy: int = 0) -> None: return self._display.scroll(dx, dy)
    def flip(self) -> None: pygame.display.flip()