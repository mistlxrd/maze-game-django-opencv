from django.db import migrations, models


def adaptar_a_laberinto_grande(apps, schema_editor):
    # Las paredes guardadas eran de la cuadrícula anterior (celdas de 100 px): se borran
    # y el juego genera un laberinto nuevo de 20x10 la próxima vez que se dibuje.
    apps.get_model('backend', 'Pared').objects.all().delete()
    # Paso más corto para poder entrar en pasillos de 45 px y todos vuelven al inicio
    apps.get_model('backend', 'Personaje').objects.update(x=10, y=10, velocidad=10)
    apps.get_model('backend', 'PersonajeSeleccionado').objects.update(laberinto_completado=False)


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_personajeseleccionado_laberinto_completado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaje',
            name='velocidad',
            field=models.IntegerField(default=10),
        ),
        migrations.RunPython(adaptar_a_laberinto_grande, migrations.RunPython.noop),
    ]
