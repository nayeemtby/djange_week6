# Generated by Django 5.0.2 on 2024-02-10 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_borrowrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowrecord',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='borrowDate',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='returned',
            field=models.BooleanField(default=False),
        ),
    ]
