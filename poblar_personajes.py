import os
from pathlib import Path
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'juego.settings')
django.setup()

from django.contrib.auth import get_user_model
from backend.models import Personaje, PersonajeSeleccionado

BASE_DIR = Path(__file__).resolve().parent

PERSONAJES = {
    "pepe": "personaje.png",
    "samael": "unnamed.jpg",
    "Don M": "dxcmkj8eb7yic_600.jpg",
    "perro del enfasis": "perro_del_enfasis.jpg",
    "perro enfasis": "perro_enfasis.jpeg",
    "perro piruleta": "perro_piruleta.jpg",
    "perro cowboy": "perro_cowboy.jpg",
}

for nombre, archivo in PERSONAJES.items():
    if not (BASE_DIR / "static" / archivo).exists():
        raise FileNotFoundError(f"Falta static/{archivo}")

    # Solo actualiza la imagen; la posición guardada no se toca si el personaje ya existe
    Personaje.objects.update_or_create(
        nombre=nombre,
        defaults={"imagen": (Path("static") / archivo).as_posix()},
        create_defaults={
            "x": 13,  # dentro de la primera celda del laberinto
            "y": 13,
            "velocidad": 15,
            "imagen": (Path("static") / archivo).as_posix(),
        },
    )

if not PersonajeSeleccionado.objects.exists():
    PersonajeSeleccionado.objects.create(seleccionado=Personaje.objects.first())

User = get_user_model()
usuario, _ = User.objects.get_or_create(username="alumno")
usuario.is_staff = True
usuario.is_superuser = True
usuario.set_password("usm1234")
usuario.save()
