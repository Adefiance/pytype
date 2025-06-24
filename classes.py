from simple import *
import typing
import pygame

class DrawWrapper:
    def __init__(self, surface: pygame.surface.Surface): self.surface = surface
    def rect(self, color: ColorValue, rect: RectValue, width: int = 0): pygame.draw.rect(self.surface, color, rect, width)
    def polygon(self, color: ColorValue, points: PolyValue, width: int = 0): pygame.draw.polygon(self.surface, color, points, width)
    def circle(self, color: ColorValue, center: Coordinate, radius: int, width: int = 0): pygame.draw.circle(self.surface, color, center, radius, width)
    def ellipse(self, color: ColorValue, rect: RectValue, width: int = 0): pygame.draw.ellipse(self.surface, color, rect, width)
    def arc(self, color: ColorValue, rect: RectValue, start_angle: int, stop_angle: int, width: int = 1): pygame.draw.arc(self.surface, color, rect, start_angle, stop_angle, width)
    def line(self, color: ColorValue, start: Coordinate, end: Coordinate, width: int = 1): pygame.draw.line(self.surface, color, start, end, width)
    def lines(self, color: ColorValue, closed: anyBool, points: PolyValue, width: int = 1): pygame.draw.lines(self.surface, color, bool(closed), points, width)
    def aaline(self, color, start: Coordinate, end: Coordinate, blend: int = 1): pygame.draw.aaline(self.surface, color, start, end, blend)
    def aalines(self, color, closed: anyBool, points: PolyValue, blend: int = 1): pygame.draw.aalines(self.surface, color, bool(closed), points, blend)

class Surface:
    def __init__(self, size: Coordinate, flags: int = 0, depth: int = 0, masks: ColorValue | None = None):
        if depth != 0:
            if masks is None: raise ValueError("If you specify a nonzero depth, you must also specify masks")
            self._surf = pygame.Surface(size, flags, depth, masks)
        else: self._surf = pygame.Surface(size, flags)
        self.draw = DrawWrapper(self._surf)
    def scaleBy(self, size: int) -> None: self._surf = pygame.transform.smoothscale(self._surf, (self._surf.get_size()[0] * size, self._surf.get_size()[1] * size))
    def scale(self, size: Coordinate) -> None: self._surf = pygame.transform.smoothscale(self._surf, size)
    def rotate(self, degree: int) -> None: self._surf = pygame.transform.rotate(pygame.transform.smoothscale(self._surf, self._surf.get_size()), degree)
    def flip(self, x: anyBool = False, y: anyBool = False) -> None: self._surf = pygame.transform.flip(self._surf, x, y)
    def isAlpha(self) -> bool: return self._surf.get_alpha() != None
    def convertAlpha(self) -> None: self._surf = self._surf.convert_alpha()
    def getSurface(self) -> pygame.surface.Surface: return self._surf
    def blit(self, source: pygame.surface.Surface, dest: Coordinate | RectValue, area: RectValue | None = None, flags: int = 0) -> pygame.Rect: return self._surf.blit(source, dest, area, flags)
    def blits(self, sequence: typing.Sequence[ typing.Union[ typing.Tuple[pygame.surface.Surface, typing.Union[Coordinate, RectValue]], typing.Tuple[pygame.surface.Surface, typing.Union[Coordinate, RectValue], typing.Union[RectValue, int]], typing.Tuple[pygame.surface.Surface, typing.Union[Coordinate, RectValue], RectValue, int] ] ], doreturn: anyBool = 1) -> list[pygame.Rect] | None: return self._surf.blits(sequence, doreturn)
    def copy(self): return self

    __copy__ = copy
    
class Rect (pygame.Rect):
    def onSurface(self: pygame.Rect, color: ColorValue, flags: int = 0, depth: int = 32, masks: ColorValue | None = None) -> Surface:
        surface: Surface = Surface(self.size, flags, depth, masks)
        pygame.draw.rect(surface.getSurface(), color, pygame.Rect((0, 0), self.size))
        return surface

class Display:
    def __init__(self, size: Coordinate = (0, 0), flags: int = 0, depth: int = 0, display: int = 0, vsync: int = 0):
        self._display = pygame.display.set_mode(size, flags, depth, display, vsync)
        self.draw = DrawWrapper(self._display)
    def getDisplay(self) -> pygame.surface.Surface: return self._display
    def quit(self) -> None: return pygame.display.quit()
    def blit(self, source: pygame.surface.Surface, dest: Coordinate | RectValue, area: RectValue | None = None, flags: int = 0) -> pygame.Rect: return self._display.blit(source, dest, area, flags)
    def blits(self, sequence: typing.Sequence[ typing.Union[ typing.Tuple[pygame.surface.Surface, typing.Union[Coordinate, RectValue]], typing.Tuple[pygame.surface.Surface, typing.Union[Coordinate, RectValue], typing.Union[RectValue, int]], typing.Tuple[pygame.surface.Surface, typing.Union[Coordinate, RectValue], RectValue, int] ] ], doreturn: anyBool = 1) -> list[pygame.Rect] | None: return self._display.blits(sequence, doreturn)
    def copy(self): return self

    __copy__ = copy