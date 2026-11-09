from django.db import migrations


def renombrar(apps, schema_editor):
    # Solo toca bases que ya tenían a este perro; en una base nueva no hace nada
    Personaje = apps.get_model('backend', 'Personaje')
    Personaje.objects.filter(nombre="perro del enfasis").update(
        nombre="perro del ki", imagen="static/perro_del_ki.jpg"
    )


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_renombrar_perros'),
    ]

    operations = [
        migrations.RunPython(renombrar, migrations.RunPython.noop),
    ]
