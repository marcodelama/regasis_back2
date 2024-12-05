# Generated by Django 4.2.16 on 2024-12-05 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reconocimientoFacial', '0002_asistencia_dependencia_espacioaula_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripción', models.ImageField(upload_to='personas/')),
            ],
        ),
    ]