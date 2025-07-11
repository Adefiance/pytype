from pytype.simple import ColorValue, RectValue, PolyValue, Coordinate, AnyBool, AlphaValue
import typing
import pygame

class Draw:
    def __init__(self, surface: pygame.Surface): self.__surf = surface
    def rect(self, color: ColorValue, rect: RectValue, width: int = 0): return pygame.draw.rect(self.__surf, color, rect, width)
    def polygon(self, color: ColorValue, points: PolyValue, width: int = 0): return pygame.draw.polygon(self.__surf, color, points, width)
    def circle(self, color: ColorValue, center: Coordinate, radius: int, width: int = 0): return pygame.draw.circle(self.__surf, color, center, radius, width)
    def ellipse(self, color: ColorValue, rect: RectValue, width: int = 0): return pygame.draw.ellipse(self.__surf, color, rect, width)
    def arc(self, color: ColorValue, rect: RectValue, start_angle: int, stop_angle: int, width: int = 1): return pygame.draw.arc(self.__surf, color, rect, start_angle, stop_angle, width)
    def line(self, color: ColorValue, start: Coordinate, end: Coordinate, width: int = 1): return pygame.draw.line(self.__surf, color, start, end, width)
    def lines(self, color: ColorValue, closed: AnyBool, points: PolyValue, width: int = 1): return pygame.draw.lines(self.__surf, color, bool(closed), points, width)
    def aaline(self, color, start: Coordinate, end: Coordinate, blend: int = 1): return pygame.draw.aaline(self.__surf, color, start, end, blend)
    def aalines(self, color, closed: AnyBool, points: PolyValue, blend: int = 1): return pygame.draw.aalines(self.__surf, color, bool(closed), points, blend)

class PSurface (pygame.Surface):
    def __init__(self, size: Coordinate, flags: int = 0, depth: int = 0, masks: ColorValue | None = None):
        if not depth and not masks: super().__init__(size, flags)
        elif depth and not masks: raise ValueError("No value was given for masks.")
        elif not depth and masks: raise ValueError("No value was given for depth.")
        else: super().__init__(size, flags, depth, masks)
        self.draw = Draw(self)
class PRect (pygame.Rect):
    def on_surface(self: pygame.Rect, color: ColorValue, flags: int = 0, depth: int = 0, masks: AlphaValue | None = None, width: int = 0) -> PSurface:
        """Returns the Rect on a pytype Surface of its size."""
        if masks is not None: surface = PSurface(self.size, flags, depth, masks)
        else: surface = PSurface(self.size, flags)
        surface.draw.rect(color, pygame.Rect((0, 0), self.size), width)
        return surface
    def on_dsurface(self: pygame.Rect, color: ColorValue, flags: int = 0, depth: int = 0, masks: AlphaValue | None = None, width: int = 0) -> pygame.Surface:
        """Returns the Rect on a pygame Surface of its size."""
        if masks is not None: surface = pygame.Surface(self.size, flags, depth, masks)
        else: surface = pygame.Surface(self.size, flags, 32)
        pygame.draw.rect(surface, color, pygame.Rect((0, 0), self.size), width)
        return surface
class PDisplay:
    def __init__(self, size: Coordinate = (0, 0), flags: int = 0, depth: int = 0, display: int = 0, vsync: int = 0):
        self.display = pygame.display.set_mode(size, flags, depth, display, vsync)
        self.__index = display
        self.__vsync = vsync
        self.draw = Draw(self.display)
    def quit(self) -> None:
        pygame.display.quit()
        self.display = None
        self.draw = None
        self.__index = None
        self.__vsync = None
    def blit(self, source: pygame.Surface, dest: Coordinate | RectValue, area: RectValue | None = None, flags: int = 0) -> pygame.Rect: 
        if self.display: return self.display.blit(source, dest, area, flags)
        else: raise AttributeError("This display has been killed.")
    def blits(self, sequence: typing.Sequence[ typing.Union[ typing.Tuple[pygame.Surface, typing.Union[Coordinate, RectValue]], typing.Tuple[pygame.Surface, typing.Union[Coordinate, RectValue], typing.Union[RectValue, int]], typing.Tuple[pygame.Surface, typing.Union[Coordinate, RectValue], RectValue, int] ] ], doreturn: AnyBool = 1) -> list[pygame.Rect] | None: 
        if self.display: return self.display.blits(sequence, doreturn)
        else: raise AttributeError("This display has been killed.")
    def resize(self, size: Coordinate, scale: tuple[AnyBool, AnyBool] = (False, False)) -> None:
        if self.display and self.__index and self.__vsync:
            old = self.display.copy()
            new = pygame.display.set_mode(size, self.display.get_flags(), self.display.get_bitsize(), self.__index, self.__vsync)

            self.display = new
            self.draw = Draw(new)

            scaled = pygame.transform.scale(old, (new.get_size()[0] if scale[0] else old.get_size()[0], new.get_size()[1] if scale[1] else old.get_size()[1]))
            self.blit(scaled, (0, 0))
        else: raise AttributeError("This display has been killed.")
    def scroll(self, dx: int = 0, dy: int = 0) -> None: 
        if self.display: self.display.scroll(dx, dy)
        else: raise AttributeError("This display has been killed.")
    def flip(self) -> None: 
        if self.display: pygame.display.flip()
        else: raise AttributeError("This display has been killed.")
class PFont (pygame.font.Font):
    def p_render(self, text: str | bytes, antialias: AnyBool, color: ColorValue, background: ColorValue | None = None, flags: int = 0, depth: int = 0, masks: ColorValue | None = None):
        surface = self.render(text, antialias, color, background)
        psurface = PSurface(surface.get_size(), flags, depth, masks)
        psurface.blit(surface, (0, 0))
        return psurface