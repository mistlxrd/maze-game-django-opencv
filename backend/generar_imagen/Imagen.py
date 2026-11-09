from backend.generar_imagen.Laberinto import CELDA_W, CELDA_H, COLS, FILAS


class Imagen:
    def __init__(self):
        # Tamaño del lienzo: el mismo de la cuadrícula del laberinto (1080 x 540)
        self.W = COLS * CELDA_W
        self.H = FILAS * CELDA_H
