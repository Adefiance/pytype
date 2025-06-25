# Pytype - Make pygame a little easier, maybe.

Welcome to pytype, a VERY simple module that allows you a slightly easier time making something out of pygame!
In this, we have:

## Typing - Some simple types
If you look into the `simple.py` file, you will find a few types, mostly relating to pygame, except one called "anyBool".

`anyBool` - Did you know booleans are actually a **subclass** of numbers? Because of this, we can very easily tie 0 to False and 1 to True. Because of that, we can use this type for a more lenient experience with methods and typing.

`ColorValue` - This type will only allow RGB/A values, as this is mainly what pygame accepts as a color value.

`AlphaValue` - This is a specific version. Made to only accept color values that include a transparency value. Used for arguments like pygame.Surface's masks and an alpha surface!

`Coordinate` - This is used for 2D positioning and sizes. It only accepts a tuple of 2 integers.

`RectValue` - Anything compatible with pygame.Rect. For example, a 4-integer tuple, or a tuple of 2 tuples each with 2 integers, or just straight up an actual pygame.Rect object.

`PolyValue` - Anything compatible a pygame polygon. Only accepts tuples with 3 or more of `Coordinate`

## Classes - Where the fun is at!
Taking a peek at the `classes.py` file, you can see a few classes, such as `Display` and `DrawWrapper`.

`DrawWrapper` - As the name suggest this is a wrapper. For what? The `Surface` and `Display` classes! This allows them to access pygame.draw from themself, already setting the first argument, the surface as the `Surface`/`Display` Instance.

`Surface` - A (kind of) better way to make and set a pygame Surface. Comes with some transformations for the user, such as `.convertAlpha` or `scaleBy`. From `.draw`, you can draw something onto the surface from there.

`Rect` - A simple extension of pygame's `Rect` object, but now coming with an `onSurface` and `onTrueSurface` method. This allows the user to get the Rect object as a surface of the original Rect's size in a singular line. `onSurface` will return the **pytype** version of a `Surface`, while `onTrueSurface` returns a real and normal pygame surface.

`Display` - On call, this creates a window with the flags, depth and other arguments you would put in a normal display window. However, now you have access to `.draw`, as mentioned before, and `.resize`, which will resize the window at any size you wish.

I genuinelly hope you find my package useful ^_^ Just make sure not to run code from the package itself!