# Generated by Django 5.1.7 on 2025-04-25 15:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fynder', '0005_fynder_is_vegan_fynder_is_vegetarian_foodpreference_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=100)),
                ('interest_culture_heritage', models.FloatField(default=0.0, help_text='Interest level in Culture & Heritage (0-0.5-1)')),
                ('interest_nature_outdoors', models.FloatField(default=0.0, help_text='Interest level in Nature & Outdoors (0-0.5-1)')),
                ('interest_food_gastronomy', models.FloatField(default=0.0, help_text='Interest level in Food & Gastronomy (0-0.5-1)')),
                ('interest_nightlife_party', models.FloatField(default=0.0, help_text='Interest level in Nightlife & Party (0-0.5-1)')),
                ('interest_wellness_spa', models.FloatField(default=0.0, help_text='Interest level in Wellness & Spa (0-0.5-1)')),
                ('interest_sport_adventure', models.FloatField(default=0.0, help_text='Interest level in Sport & Adventure (0-0.5-1)')),
                ('interest_music_festivals', models.FloatField(default=0.0, help_text='Interest level in Music & Festivals (0-0.5-1)')),
                ('interest_shopping_fashion', models.FloatField(default=0.0, help_text='Interest level in Shopping & Fashion (0-0.5-1)')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('weight', models.FloatField(default=1.0)),
            ],
        ),
        migrations.AlterField(
            model_name='foodpreference',
            name='label',
            field=models.CharField(choices=[('Any', 'Any'), ('Pescatarian', 'Pescatarian'), ('Halal', 'Halal'), ('Kosher', 'Kosher')], default='any', max_length=20),
        ),
        migrations.CreateModel(
            name='FynderAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fynder.answer')),
                ('fynder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fynder.question'),
        ),
    ]
