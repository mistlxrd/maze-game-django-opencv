from django.shortcuts import render, get_object_or_404
from backend.models import Personaje, PersonajeSeleccionado, Pared
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from backend.generar_imagen.Jugador import Jugador
from backend.generar_imagen.Laberinto import Laberinto

import os
import numpy as np
import json
import cv2 

W = 1000
H = 500
PATH = os.getcwd()
TAM_PERSONAJE = 30
INICIO_X, INICIO_Y = 10, 10  # dentro de la primera celda
# Create your views here.
def dibujar_linea_horizontal(img, x_inicio, y, largo, grosor=5, color=(100, 200, 100)):                                                                                  
        for x in range(x_inicio, x_inicio + largo):                                                                                                                          
            #Punto inicial: (x, y)
            # Punto final: (x, y + grosor)  <- pequeña línea vertical
            cv2.line(img, (x, y), (x, y + grosor), color, 1)

def recortar_cuadrado(img):
    # Recorta el centro de la imagen para que sea cuadrada y no se deforme al escalar
    alto, ancho = img.shape[:2]
    lado = min(alto, ancho)
    y0 = (alto - lado) // 2
    x0 = (ancho - lado) // 2
    return img[y0:y0 + lado, x0:x0 + lado]

def nuevo_laberinto(ps):
    Laberinto().reiniciar()
    # El laberinto cambió: todos los personajes vuelven al inicio
    Personaje.objects.update(x=INICIO_X, y=INICIO_Y)
    ps.laberinto_completado = False
    ps.save()

def seleccion_personaje(request):
    # Al salir del tablero con el laberinto completado, se crea uno nuevo
    ps = PersonajeSeleccionado.objects.first()
    if ps and ps.laberinto_completado:
        nuevo_laberinto(ps)

    personajes_db = Personaje.objects.order_by("id")
    
    personajes = []
    
    for p in personajes_db:
        foo = {
            "id": p.id,
            "nombre": p.nombre,
            "imagen_url": p.imagen.url
        }
        
        personajes.append(foo)
        
    return render(request, "seleccion_personaje.html", {
        "personajes": personajes,
        # El carrusel parte mostrando al personaje elegido actualmente
        "seleccionado_id": ps.seleccionado.id if ps else None,
    })

@require_POST
def seleccionar_personaje(request, id):
    personaje = get_object_or_404(Personaje, id=id)
    ps = PersonajeSeleccionado.objects.first()

    # Laberinto nuevo solo si no hay uno o si el anterior se completó
    hay_que_crear = ps is None or ps.laberinto_completado or Pared.objects.count() == 0

    if ps:
        ps.seleccionado = personaje
    else:
        ps = PersonajeSeleccionado(seleccionado=personaje)
    ps.save()

    if hay_que_crear:
        nuevo_laberinto(ps)

    return JsonResponse({"id": personaje.id, "nombre": personaje.nombre, "nuevo_laberinto": hay_que_crear})

def generar_imagen(request):
        ps = PersonajeSeleccionado.objects.first()
        p = ps.seleccionado
        jugador = Jugador(p)
        laberinto = Laberinto()
        key = request.GET.get("tecla", "")

        # El personaje debe ser más chico que una celda (50x50) para pasar por los pasillos
        personaje = cv2.imread(PATH + p.imagen.url)
        personaje = recortar_cuadrado(personaje)
        personaje = cv2.resize(personaje, (TAM_PERSONAJE, TAM_PERSONAJE))

        x, y = p.x, p.y

        # Tesoro en la última celda (abajo a la derecha)
        tesoro = cv2.imread("tesoro.jpg")
        tesoro = cv2.resize(tesoro, (TAM_PERSONAJE, TAM_PERSONAJE))
        tx, ty = 960, 460

        # Lienzo blanco donde se dibuja todo
        img = np.full((H, W, 3), 255, dtype=np.uint8)
        # 1. Dibujar laberinto y tesoro
        laberinto.dibujar(img)
        img[ty:ty+tesoro.shape[0], tx:tx+tesoro.shape[1]] = tesoro

        # 2. Intento de movimiento
        ancho_p = personaje.shape[1]
        alto_p = personaje.shape[0]
        x_nuevo, y_nuevo = jugador.movimiento_personaje(key, ancho_p, alto_p, W, H)

        # 3. Colisión con las paredes del laberinto usando min/max (queda al ras de la pared)
        x_nuevo, y_nuevo = laberinto.resolver_colision(x, y, x_nuevo, y_nuevo, ancho_p, alto_p, key, jugador.velocidad)

        # 4. Guardar posición
        x, y = x_nuevo, y_nuevo
        p.x = x
        p.y = y
        p.save()

        # 5. ¿Llegó al tesoro? -> laberinto completado
        if jugador.hay_colision(x, y, ancho_p, alto_p, tx, ty, tesoro.shape[1], tesoro.shape[0]):
            if not ps.laberinto_completado:
                ps.laberinto_completado = True
                ps.save()

        # 6. Dibujar al personaje en su posición final
        img[y:y+alto_p, x:x+ancho_p] = personaje

        if ps.laberinto_completado:
            cv2.putText(img, "Laberinto completado!", (280, 260), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

        # 7. Responder imagen
        ok, buffer = cv2.imencode(".jpg", img)
        return HttpResponse(buffer.tobytes(), content_type="image/jpg")

def tablero(request):
    return render(request, "tablero.html")