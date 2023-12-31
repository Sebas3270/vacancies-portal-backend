# Generated by Django 4.1.7 on 2023-03-12 03:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0002_alter_vacancy_last_date_alter_vacancy_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 27, 3, 36, 51, 376575)),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='vacancyType',
            field=models.CharField(choices=[('Permanent', 'Permanent'), ('Temporary', 'Temporary'), ('Internship', 'Internship')], default='Permanent', max_length=10),
        ),
    ]
