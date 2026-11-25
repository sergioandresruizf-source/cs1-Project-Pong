"""Visual resources like text font() or sprites"""
import os
import pygame

# Folder with PNG images (src/assets).
CARPETA_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# Split the characters in PONGfont.png.
# Every row has 8 characters.
ORDEN = (
    "ABCDEFGH"
    "IJKLMNOP"
    "QRSTUVWX"
    "YZ123456"
    "7890,.-_"
    "@/*+%'#!"
    "¡?¿\\&\":;"  #Here we use \ for avoid strings issues
    "=←↓→↑|()"
)


def cargar_imagen(nombre, tamaño=None):
    """Charge image from assets/ and give scale"""
    img = pygame.image.load(os.path.join(CARPETA_ASSETS, nombre)).convert_alpha()
    if tamaño is not None:
        img = pygame.transform.scale(img, tamaño)
    return img


def teñir(img, color):
    """Give the possibility of paint the sprites with (R,G,B)"""
    copia = img.copy()
    copia.fill(color + (255,), special_flags=pygame.BLEND_RGBA_MULT)
    return copia


class FuentePixel:
    """Write text with image format (spritesheet)."""

    def __init__(self, nombre, escala=4, celda=16, columnas=8):
        hoja = cargar_imagen(nombre)
        self.ancho = celda * escala
        self.letras = {}
        for i, ch in enumerate(ORDEN):
            x = (i % columnas) * celda
            y = (i // columnas) * celda
            glifo = hoja.subsurface((x, y, celda, celda))
            self.letras[ch] = pygame.transform.scale(glifo, (self.ancho, self.ancho))

    def render(self, texto, color=(255, 255, 255)):
        texto = texto.upper()
        sup = pygame.Surface((len(texto) * self.ancho, self.ancho), pygame.SRCALPHA)
        for i, ch in enumerate(texto):
            if ch in self.letras:
                sup.blit(self.letras[ch], (i * self.ancho, 0))
        if color != (255, 255, 255):
            sup = teñir(sup, color)
        return sup