"""Recursos visuales del juego: fuente de pixel art e imágenes (sprites)."""
import os
import pygame

# Carpeta donde están las imágenes (src/assets), sin importar desde dónde se ejecute el juego.
CARPETA_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# Orden de los caracteres en PONGfont.png: de izquierda a derecha y de arriba abajo.
# Cada línea es una fila de la imagen (8 caracteres por fila).
ORDEN = (
    "ABCDEFGH"
    "IJKLMNOP"
    "QRSTUVWX"
    "YZ123456"
    "7890,.-_"
    "@/*+%'#!"
    "¡?¿\\&\":;"
    "=←↓→↑|()"
)


def cargar_imagen(nombre, tamaño=None):
    """Carga una imagen de assets/ y, si se pide, la escala a (ancho, alto)."""
    img = pygame.image.load(os.path.join(CARPETA_ASSETS, nombre)).convert_alpha()
    if tamaño is not None:
        img = pygame.transform.scale(img, tamaño)
    return img


def teñir(img, color):
    """Devuelve una copia de una imagen blanca pintada del color (R, G, B)."""
    copia = img.copy()
    copia.fill(color + (255,), special_flags=pygame.BLEND_RGBA_MULT)
    return copia


class FuentePixel:
    """Escribe textos usando las letras dibujadas en una imagen (spritesheet)."""

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