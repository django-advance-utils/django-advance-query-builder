# Generated by Django 3.2.7 on 2022-02-07 15:37

from django.db import migrations, models
import django.db.models.deletion
import time_stamped_model.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', time_stamped_model.models.CreationDateTimeField(auto_now_add=True)),
                ('modified', time_stamped_model.models.ModificationDateTimeField(auto_now=True)),
                ('slug', models.SlugField(unique=True)),
                ('slug_alias', models.SlugField(blank=True, null=True)),
                ('name', models.CharField(max_length=200)),
                ('display_option', models.PositiveIntegerField(choices=[(1, '1 Report per Row'), (2, '2 Reports per Row'), (3, '3 Reports per Row'), (4, '4 Reports per Row')], default=2)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', time_stamped_model.models.CreationDateTimeField(auto_now_add=True)),
                ('modified', time_stamped_model.models.ModificationDateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('slug_alias', models.SlugField(blank=True, null=True)),
                ('instance_type', models.CharField(max_length=255, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('version', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ReportTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', time_stamped_model.models.CreationDateTimeField(auto_now_add=True)),
                ('modified', time_stamped_model.models.ModificationDateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('order', models.PositiveSmallIntegerField()),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='BarChartReport',
            fields=[
                ('report_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='advanced_report_builder.report')),
                ('axis_scale', models.PositiveSmallIntegerField(choices=[(1, 'Year'), (2, 'Quarter'), (3, 'Month'), (4, 'Week'), (5, 'Day')])),
                ('date_field', models.CharField(max_length=200)),
                ('axis_value_type', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Sum'), (2, 'Max'), (3, 'Min'), (4, 'Count'), (5, 'Avg')], default=4, null=True)),
                ('fields', models.JSONField(blank=True, null=True)),
                ('x_label', models.CharField(blank=True, max_length=200, null=True)),
                ('y_label', models.CharField(blank=True, max_length=200, null=True)),
                ('bar_chart_orientation', models.PositiveSmallIntegerField(choices=[(1, 'Vertical'), (2, 'Horizontal')], default=1)),
                ('stacked', models.BooleanField(default=False)),
                ('show_totals', models.BooleanField(default=False)),
                ('show_blank_dates', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('advanced_report_builder.report',),
        ),
        migrations.CreateModel(
            name='FunnelChartReport',
            fields=[
                ('report_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='advanced_report_builder.report')),
                ('axis_value_type', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Sum'), (2, 'Max'), (3, 'Min'), (4, 'Count'), (5, 'Avg')], default=4, null=True)),
                ('fields', models.JSONField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('advanced_report_builder.report',),
        ),
        migrations.CreateModel(
            name='KanbanReport',
            fields=[
                ('report_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='advanced_report_builder.report')),
            ],
            options={
                'abstract': False,
            },
            bases=('advanced_report_builder.report',),
        ),
        migrations.CreateModel(
            name='LineChartReport',
            fields=[
                ('report_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='advanced_report_builder.report')),
                ('axis_scale', models.PositiveSmallIntegerField(choices=[(1, 'Year'), (2, 'Quarter'), (3, 'Month'), (4, 'Week'), (5, 'Day')])),
                ('date_field', models.CharField(max_length=200)),
                ('axis_value_type', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Sum'), (2, 'Max'), (3, 'Min'), (4, 'Count'), (5, 'Avg')], default=4, null=True)),
                ('fields', models.JSONField(blank=True, null=True)),
                ('x_label', models.CharField(blank=True, max_length=200, null=True)),
                ('y_label', models.CharField(blank=True, max_length=200, null=True)),
                ('show_totals', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('advanced_report_builder.report',),
        ),
        migrations.CreateModel(
            name='PieChartReport',
            fields=[
                ('report_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='advanced_report_builder.report')),
                ('axis_value_type', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Sum'), (2, 'Max'), (3, 'Min'), (4, 'Count'), (5, 'Avg')], default=4, null=True)),
                ('fields', models.JSONField(blank=True, null=True)),
                ('style', models.PositiveSmallIntegerField(choices=[(1, 'Pie'), (2, 'Doughnut')], default=1)),
            ],
            options={
                'abstract': False,
            },
            bases=('advanced_report_builder.report',),
        ),
        migrations.CreateModel(
            name='SingleValueReport',
            fields=[
                ('report_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='advanced_report_builder.report')),
                ('tile_colour', models.CharField(blank=True, max_length=10, null=True)),
                ('field', models.CharField(blank=True, max_length=200, null=True)),
                ('numerator', models.CharField(blank=True, max_length=200, null=True)),
                ('single_value_type', models.PositiveSmallIntegerField(choices=[(1, 'Count'), (2, 'Sum'), (3, 'Count & Sum'), (4, 'Percent'), (5, 'Percent from Count'), (6, 'Average')], default=1)),
                ('prefix', models.CharField(blank=True, max_length=64, null=True)),
                ('decimal_places', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=('advanced_report_builder.report',),
        ),
        migrations.CreateModel(
            name='TableReport',
            fields=[
                ('report_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='advanced_report_builder.report')),
                ('table_fields', models.JSONField(blank=True, null=True)),
                ('has_clickable_rows', models.BooleanField(default=False)),
                ('link_field', models.CharField(blank=True, max_length=200, null=True)),
                ('pivot_fields', models.JSONField(blank=True, null=True)),
                ('page_length', models.PositiveSmallIntegerField(choices=[(10, '10'), (25, '25'), (50, '50'), (100, '100'), (150, '150'), (200, '200')], default=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('advanced_report_builder.report',),
        ),
        migrations.CreateModel(
            name='ReportType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', time_stamped_model.models.CreationDateTimeField(auto_now_add=True)),
                ('modified', time_stamped_model.models.ModificationDateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('report_builder_class_name', models.CharField(max_length=200)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.contenttype')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='report',
            name='report_tags',
            field=models.ManyToManyField(blank=True, to='advanced_report_builder.ReportTag'),
        ),
        migrations.AddField(
            model_name='report',
            name='report_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='advanced_report_builder.reporttype'),
        ),
        migrations.CreateModel(
            name='DashboardReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', time_stamped_model.models.CreationDateTimeField(auto_now_add=True)),
                ('modified', time_stamped_model.models.ModificationDateTimeField(auto_now=True)),
                ('order', models.PositiveSmallIntegerField()),
                ('top', models.BooleanField(default=False)),
                ('name_override', models.CharField(blank=True, max_length=200, null=True)),
                ('display_option', models.PositiveIntegerField(choices=[(0, 'None/Default'), (1, '1 Report per Row'), (2, '2 Reports per Row'), (3, '3 Reports per Row'), (4, '4 Reports per Row')], default=0)),
                ('dashboard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advanced_report_builder.dashboard')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advanced_report_builder.report')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='ReportQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', time_stamped_model.models.CreationDateTimeField(auto_now_add=True)),
                ('modified', time_stamped_model.models.ModificationDateTimeField(auto_now=True)),
                ('name', models.TextField(default='Standard')),
                ('query', models.JSONField(blank=True, null=True)),
                ('extra_query', models.JSONField(blank=True, null=True)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advanced_report_builder.report')),
            ],
            options={
                'verbose_name_plural': 'Report queries',
                'ordering': ['name'],
                'unique_together': {('name', 'report')},
            },
        ),
        migrations.CreateModel(
            name='KanbanReportLane',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', time_stamped_model.models.CreationDateTimeField(auto_now_add=True)),
                ('modified', time_stamped_model.models.ModificationDateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('order', models.PositiveSmallIntegerField()),
                ('heading_field', models.CharField(blank=True, max_length=200, null=True)),
                ('order_by_field', models.CharField(blank=True, max_length=200, null=True)),
                ('link_field', models.CharField(blank=True, max_length=200, null=True)),
                ('order_by_ascending', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('query_data', models.JSONField(blank=True, null=True)),
                ('report_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='advanced_report_builder.reporttype')),
                ('kanban_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advanced_report_builder.kanbanreport')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
