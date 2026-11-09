from django.db import migrations, models


def adaptar_a_laberinto_medio(apps, schema_editor):
    # Las paredes guardadas eran de la cuadrícula anterior (celdas de 50 px): se borran
    # y el juego genera un laberinto nuevo de 18x9 la próxima vez que se dibuje.
    apps.get_model('backend', 'Pared').objects.all().delete()
    # Paso de 15 px (4 pasos = 1 celda de 60 px) y todos vuelven al inicio
    apps.get_model('backend', 'Personaje').objects.update(x=13, y=13, velocidad=15)
    apps.get_model('backend', 'PersonajeSeleccionado').objects.update(laberinto_completado=False)


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_laberinto_mas_grande'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaje',
            name='velocidad',
            field=models.IntegerField(default=15),
        ),
        migrations.RunPython(adaptar_a_laberinto_medio, migrations.RunPython.noop),
    ]
