# Generated by Django 3.2.7 on 2022-01-20 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advanced_report_builder', '0002_auto_20220120_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='singlevaluereport',
            name='prefix',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
