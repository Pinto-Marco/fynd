# Generated by Django 5.1.7 on 2025-04-25 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fynder', '0007_rename_foodpreference_fynderfoodpreference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer_text',
            field=models.CharField(max_length=200),
        ),
    ]
