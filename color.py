WHITE=(255, 255, 255)
RED=(255, 0, 0)
GREEN=(0, 255, 0)
BLUE=(0, 0, 255)
BLACK=(0,0,0)

def str_to_color(colorstr: str):
    if colorstr=="WHITE":
        return WHITE
    elif colorstr=="BLACK":
        return BLACK
    elif colorstr=="RED":
        return RED
    elif colorstr == "GREEN":
        return GREEN
    elif colorstr == "BLUE":
        return BLUE
