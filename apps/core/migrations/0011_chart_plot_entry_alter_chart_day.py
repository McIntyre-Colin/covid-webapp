# Generated by Django 4.0.4 on 2022-06-29 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_chart_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='chart',
            name='plot_entry',
            field=models.BinaryField(default=None),
        ),
        migrations.AlterField(
            model_name='chart',
            name='day',
            field=models.CharField(default='01', max_length=2),
        ),
    ]
