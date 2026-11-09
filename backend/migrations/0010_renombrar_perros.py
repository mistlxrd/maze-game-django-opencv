from django.db import migrations

# nombre anterior -> (nombre nuevo, imagen nueva)
CAMBIOS = {
    "perro del kizaz enfasis": ("perro enfasis", "static/perro_enfasis.jpeg"),
    "perro vio cowboy": ("perro cowboy", "static/perro_cowboy.jpg"),
}


def renombrar(apps, schema_editor):
    # Solo toca bases que ya tenían a estos perros; en una base nueva no hace nada
    Personaje = apps.get_model('backend', 'Personaje')
    for anterior, (nuevo, imagen) in CAMBIOS.items():
        Personaje.objects.filter(nombre=anterior).update(nombre=nuevo, imagen=imagen)


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_laberinto_tamano_medio'),
    ]

    operations = [
        migrations.RunPython(renombrar, migrations.RunPython.noop),
    ]
