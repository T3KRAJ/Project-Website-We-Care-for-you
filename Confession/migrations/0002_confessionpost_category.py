# Generated by Django 3.0.6 on 2020-06-11 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Confession', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='confessionpost',
            name='category',
            field=models.CharField(blank=True, choices=[('TR', 'Truth'), ('FA', 'Fantasy'), ('DR', 'Dream'), ('GU', 'Guilt'), ('LI', 'Lie'), ('PA', 'Pain'), ('RA', 'Random Feeling'), ('FE', 'First Experience'), ('WI', 'Wild Experience')], max_length=2, null=True),
        ),
    ]
