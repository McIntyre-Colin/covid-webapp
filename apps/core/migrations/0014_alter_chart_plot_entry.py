# Generated by Django 4.0.4 on 2022-07-01 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_chart_plot_entry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='plot_entry',
            field=models.CharField(default='', max_length=1000000),
        ),
    ]
