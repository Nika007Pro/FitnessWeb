# Generated by Django 4.2.9 on 2024-01-15 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_ticket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gym',
            name='workouts',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='membership',
        ),
        migrations.DeleteModel(
            name='Card',
        ),
        migrations.DeleteModel(
            name='CardPlan',
        ),
        migrations.DeleteModel(
            name='Gym',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
        migrations.DeleteModel(
            name='Workouts',
        ),
    ]
