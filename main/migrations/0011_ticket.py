# Generated by Django 4.2.9 on 2024-01-14 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_profile_selected_membership_profile_selected_plan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_purchased', models.DateField()),
                ('membership', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.gymmembership')),
            ],
        ),
    ]
