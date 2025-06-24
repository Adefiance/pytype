from simple import *
import pygame

class DrawWrapper:
    def __init__(self, surface: pygame.surface.Surface): self.surface = surface
    def rect(self, color: ColorValue, rect: RectValue, width: int = 0): pygame.draw.rect(self.surface, color, rect, width)
    def polygon(self, color: ColorValue, points: PolyValue, width: int = 0): pygame.draw.polygon(self.surface, color, points, width)
    def circle(self, color: ColorValue, center: Coordinate, radius: int, width: int = 0): pygame.draw.circle(self.surface, color, center, radius, width)
    def ellipse(self, color: ColorValue, rect: RectValue, width: int = 0): pygame.draw.ellipse(self.surface, color, rect, width)
    def arc(self, color: ColorValue, rect: RectValue, start_angle: int, stop_angle: int, width: int = 1): pygame.draw.arc(self.surface, color, rect, start_angle, stop_angle, width)
    

class Surface (pygame.surface.Surface):
    def __init__(self, size: Coordinate, flags: int = 0, depth: int = 0, masks: ColorValue | None = None):
        if depth != 0:
            if masks is None: raise ValueError("If you specify a nonzero depth, you must also specify masks")
            self._surf = pygame.Surface(size, flags, depth, masks)
        else: self._surf = pygame.Surface(size, flags)
        self.draw = DrawWrapper(self._surf)
    def __getattr__(self, attr): return getattr(self._surf, attr)
    def scaleBy(self, size: int) -> None: self = pygame.transform.smoothscale(self, (self.get_size()[0] * size, self.get_size()[1] * size))
    def scale(self, size: Coordinate) -> None: self = pygame.transform.smoothscale(self, size)
    def rotate(self, degree: int) -> None: self = pygame.transform.rotate(pygame.transform.smoothscale(self.surf, self.get_size()), degree)
    def flip(self, x: anyBool = False, y: anyBool = False) -> None: self.surf = pygame.transform.flip(self.surf, x, y)
    def isAlpha(self) -> bool: return self.get_alpha() != None
    def convertAlpha(self) -> None: self = self.convert_alpha()
    def getSurface(self) -> pygame.surface.Surface: return self._surf
    
class Rect (pygame.Rect):
    def onSurface(self: pygame.Rect, color: ColorValue, flags: int = 0, depth: int = 32, masks: ColorValue | None = None):
        surface: Surface = Surface(self.size, flags, depth, masks)
        pygame.draw.rect(surface, color, pygame.Rect((0, 0), self.size))
        return surface