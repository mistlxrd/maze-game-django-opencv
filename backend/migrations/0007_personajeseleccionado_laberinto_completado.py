from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_pared'),
    ]

    operations = [
        migrations.AddField(
            model_name='personajeseleccionado',
            name='laberinto_completado',
            field=models.BooleanField(default=False),
        ),
    ]
