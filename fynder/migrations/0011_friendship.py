# Generated by Django 5.1.7 on 2025-04-28 18:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fynder', '0010_signupquestion_max_number_of_answers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fynder_2', to=settings.AUTH_USER_MODEL)),
                ('fynder_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fynder_1', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
