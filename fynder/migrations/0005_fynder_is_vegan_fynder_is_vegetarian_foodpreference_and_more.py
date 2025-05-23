# Generated by Django 5.1.7 on 2025-04-25 13:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fynder', '0004_remove_fynder_food_preferences'),
    ]

    operations = [
        migrations.AddField(
            model_name='fynder',
            name='is_vegan',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='fynder',
            name='is_vegetarian',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='FoodPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(choices=[('any', 'Any'), ('pescatarian', 'Pescatarian'), ('halal', 'Halal'), ('kosher', 'Kosher')], default='any', max_length=20)),
                ('fynder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='FoodPreferences',
        ),
    ]
