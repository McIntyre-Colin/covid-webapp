# Generated by Django 4.0.5 on 2022-07-04 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_alter_stateslist_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stateslist',
            name='state',
            field=models.CharField(blank=True, default='', max_length=2),
        ),
    ]