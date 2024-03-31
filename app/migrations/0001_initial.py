# Generated by Django 4.2.11 on 2024-03-31 08:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('detected_image', models.ImageField(blank=True, null=True, upload_to='detected_images/')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('local_temp', models.FloatField(blank=True, help_text='Local temperature reading', null=True)),
                ('local_humid', models.FloatField(blank=True, help_text='Local humidity reading', null=True)),
                ('comfort', models.CharField(blank=True, help_text='Comfort level descriptor', max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Sensor',
                'verbose_name_plural': 'Sensors',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Predict',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('predicted_type', models.CharField(blank=True, help_text='Type of the predicted object', max_length=255, null=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predictions', to='app.image')),
            ],
            options={
                'verbose_name': 'Prediction',
                'verbose_name_plural': 'Predictions',
                'ordering': ['id'],
            },
        ),
    ]
