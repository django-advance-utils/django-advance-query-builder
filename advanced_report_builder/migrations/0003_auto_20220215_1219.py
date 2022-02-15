# Generated by Django 3.2.7 on 2022-02-15 12:19

from django.db import migrations, models
import time_stamped_model.models


class Migration(migrations.Migration):

    dependencies = [
        ('advanced_report_builder', '0002_auto_20220209_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', time_stamped_model.models.CreationDateTimeField(auto_now_add=True)),
                ('modified', time_stamped_model.models.ModificationDateTimeField(auto_now=True)),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=64)),
                ('target_type', models.PositiveSmallIntegerField(choices=[(1, 'Count'), (2, 'Money'), (3, 'Percentage')])),
                ('colour', models.CharField(blank=True, help_text=' The colour when it gets displayed on a report', max_length=10, null=True)),
                ('default_value', models.IntegerField(default=0)),
                ('overridden', models.BooleanField(default=False)),
                ('override_data', models.JSONField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='linechartreport',
            name='has_targets',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='linechartreport',
            name='targets',
            field=models.ManyToManyField(blank=True, to='advanced_report_builder.Target'),
        ),
    ]
