import random
import cv2
from backend.models import Pared

CELDA_W = 60
CELDA_H = 60
COLS = 18
FILAS = 9
GROSOR = 5

## Dibuja linea horizontal discretizada usando segmentos verticales contiguos
def dibujar_linea_horizontal_arcaica(img, x_inicio, y, largo, grosor=GROSOR, color=(100, 200, 100)):
    for x in range(x_inicio, x_inicio + largo):
        cv2.line(img, (x, y), (x, y + grosor), color, 1)

## Dibuja linea vertical discretizada usando segmentos horizontales contiguos
def dibujar_linea_vertical_arcaica(img, x, y_inicio, alto, grosor=GROSOR, color=(100, 200, 100)):
    for y in range(y_inicio, y_inicio + alto):
        cv2.line(img, (x, y), (x + grosor, y), color, 1)

class Laberinto:
    def __init__(self):
        ## Si no hay laberinto en la base de datos, crea uno nuevo
        if Pared.objects.count() == 0:
            self.generar_nuevo()

    ## Genera laberinto procedural mediante algoritmo DFS
    def generar_nuevo(self):
        visitado = [[False for _ in range(COLS)] for _ in range(FILAS)]
        paredes_h = [[True for _ in range(COLS)] for _ in range(FILAS + 1)]
        paredes_v = [[True for _ in range(COLS + 1)] for _ in range(FILAS)]

        def dfs(f, c):
            visitado[f][c] = True
            direcciones = [(0, 1, 'E'), (0, -1, 'O'), (1, 0, 'S'), (-1, 0, 'N')]
            random.shuffle(direcciones)

            for df, dc, orientacion in direcciones:
                nf, nc = f + df, c + dc
                if 0 <= nf < FILAS and 0 <= nc < COLS and not visitado[nf][nc]:
                    if orientacion == 'E':
                        paredes_v[f][c + 1] = False
                    elif orientacion == 'O':
                        paredes_v[f][c] = False
                    elif orientacion == 'S':
                        paredes_h[f + 1][c] = False
                    elif orientacion == 'N':
                        paredes_h[f][c] = False
                    dfs(nf, nc)

        dfs(0, 0)

        ## Guarda paredes horizontales interiores en PostgreSQL
        for f in range(1, FILAS):
            for c in range(COLS):
                if paredes_h[f][c]:
                    Pared.objects.create(
                        x=c * CELDA_W,
                        y=f * CELDA_H,
                        ancho=CELDA_W,
                        alto=GROSOR
                    )

        ## Guarda paredes verticales interiores en PostgreSQL
        for f in range(FILAS):
            for c in range(1, COLS):
                if paredes_v[f][c]:
                    Pared.objects.create(
                        x=c * CELDA_W,
                        y=f * CELDA_H,
                        ancho=GROSOR,
                        alto=CELDA_H
                    )

    ## Dibuja todas las paredes activas en el lienzo de OpenCV
    def dibujar(self, img):
        for p in Pared.objects.all():
            if p.ancho > p.alto:
                dibujar_linea_horizontal_arcaica(img, p.x, p.y, p.ancho, p.alto)
            else:
                dibujar_linea_vertical_arcaica(img, p.x, p.y, p.alto, p.ancho)

    ## Ajusta posicion con min/max para quedar al ras al chocar
    def resolver_colision(self, x_actual, y_actual, x_nuevo, y_nuevo, ancho_p, alto_p, key, velocidad):
        for p in Pared.objects.all():
            solapan_x = (x_nuevo < p.x + p.ancho) and (p.x < x_nuevo + ancho_p)
            solapan_y = (y_nuevo < p.y + p.alto) and (p.y < y_nuevo + alto_p)

            if solapan_x and solapan_y:
                if key == "d":
                    x_nuevo = min(x_actual + velocidad, p.x - ancho_p)
                elif key == "a":
                    x_nuevo = max(x_actual - velocidad, p.x + p.ancho)
                elif key == "s":
                    y_nuevo = min(y_actual + velocidad, p.y - alto_p)
                elif key == "w":
                    y_nuevo = max(y_actual - velocidad, p.y + p.alto)

        return x_nuevo, y_nuevo

    ## Elimina las paredes actuales y regenera el mapa
    def reiniciar(self):
        Pared.objects.all().delete()
        self.generar_nuevo()
