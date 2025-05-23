# Generated by Django 5.1.7 on 2025-05-10 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0004_trip_status_tripfynderanswer_tripquestionanswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='from_location',
            field=models.CharField(default='ddd', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tripquestion',
            name='question_type',
            field=models.CharField(choices=[('pax', 'pax'), ('where', 'where'), ('from', 'from'), ('when', 'when'), ('budget', 'budget'), ('intensity', 'intensity')], max_length=20),
        ),
    ]
