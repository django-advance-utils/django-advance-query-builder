import base64
import json

from crispy_forms.bootstrap import StrictButton
from django.apps import apps
from django.db import ProgrammingError
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from django_datatables.datatables import DatatableTable
from django_menus.menu import MenuItem
from django_modals.forms import CrispyForm

from advanced_report_builder.columns import ReportBuilderDateColumn
from advanced_report_builder.exceptions import ReportError
from advanced_report_builder.globals import NUMBER_FIELDS, ANNOTATION_VALUE_FUNCTIONS
from advanced_report_builder.models import ReportType
from advanced_report_builder.utils import split_slug, get_django_field, split_attr
from advanced_report_builder.views.report_utils_mixin import ReportUtilsMixin
from advanced_report_builder.views.report import ReportBase


class ChartJSTable(DatatableTable):

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        self.axis_scale = kwargs.pop('axis_scale', None)
        super().__init__(*args, **kwargs)
        if pk:
            self.filter['pk'] = pk

    def model_table_setup(self):
        try:
            return mark_safe(json.dumps({'initsetup': json.loads(self.col_def_str()),
                                         'data': self.get_table_array(self.kwargs.get('request'), self.get_query()),
                                         'row_titles': self.all_titles(),
                                         'table_id': self.table_id,
                                         }))
        except ProgrammingError as e:
            raise ReportError(e)


class ChartBaseView(ReportBase, ReportUtilsMixin, TemplateView):
    # number_field = ReportBuilderNumberColumn
    date_field = ReportBuilderDateColumn
    chart_js_table = ChartJSTable

    template_name = 'advanced_report_builder/charts/report.html'

    def __init__(self, *args, **kwargs):
        self.chart_report = None
        self.show_toolbar = False
        self.table = None
        super().__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.slug = split_slug(kwargs.get('slug'))
        self.enable_edit = kwargs.get('enable_edit')
        self.dashboard_report = kwargs.get('dashboard_report')
        if self.enable_edit or (self.dashboard_report and not self.dashboard_report.top) or not self.dashboard_report:
            self.show_toolbar = True
        return super().dispatch(request, *args, **kwargs)

    def extra_filters(self, query):
        report_query = self.get_report_query(report=self.chart_report)
        if report_query:
            query = self.process_query_filters(query=query,
                                               search_filter_data=report_query.query)
        return query

    def get_date_format(self):
        return '%Y-%m-%d'

    def get_date_field(self, index, fields, base_model):

        field_name = self.chart_report.date_field
        if field_name is None:
            return

        django_field, col_type_override, _ = get_django_field(base_model=base_model, field=field_name)

        if col_type_override:
            field_name = col_type_override.field

        date_format = self.get_date_format()

        date_function_kwargs = {'title': field_name,
                                'date_format': date_format}

        annotations_value = self.chart_report.axis_scale

        new_field_name = f'{annotations_value}_{field_name}_{index}'
        function = ANNOTATION_VALUE_FUNCTIONS[annotations_value]
        date_function_kwargs['annotations_value'] = {new_field_name: function(field_name)}
        field_name = new_field_name

        date_function_kwargs.update({'field': field_name,
                                     'column_name': field_name,
                                     'model_path': ''})

        field = self.date_field(**date_function_kwargs)
        fields.append(field)
        return field_name

    @staticmethod
    def _set_multiple_title(database_values, value_prefix, fields, text):
        results = {}
        for field in fields:
            value = database_values[value_prefix + '__' + field]
            results[field] = value
        return text.format(**results)

    def process_query_results(self, base_model, table):
        fields = []
        date_field_name = self.get_date_field(0, fields, base_model=base_model)
        if date_field_name is not None:
            table.order_by = [date_field_name]
        else:
            table.order_by = ['id']

        if not self.chart_report.fields:
            return fields
        chart_fields = self.chart_report.fields
        for index, table_field in enumerate(chart_fields, 1):
            field = table_field['field']

            django_field, col_type_override, _ = get_django_field(base_model=base_model, field=field)

            if (isinstance(django_field, NUMBER_FIELDS) or
                    (col_type_override is not None and col_type_override.annotations)):
                data_attr = split_attr(table_field)
                if data_attr.get('multiple_columns') == '1':
                    query = self.extra_filters(query=table.model.objects)
                    multiple_column_field = data_attr.get('multiple_column_field')
                    report_builder_fields = getattr(base_model,
                                                    self.chart_report.report_type.report_builder_class_name, None)

                    report_builder_fields = self._get_report_builder_class(base_model=base_model,
                                                                           field_str=multiple_column_field,
                                                                           report_builder_class=report_builder_fields)
                    _fields = report_builder_fields.default_multiple_column_fields
                    default_multiple_column_fields = [multiple_column_field + '__' + x for x in _fields]
                    results = query.distinct(multiple_column_field).values(multiple_column_field,
                                                                           *default_multiple_column_fields)

                    for multiple_index, result in enumerate(results):
                        suffix = self._set_multiple_title(database_values=result,
                                                          value_prefix=multiple_column_field,
                                                          fields=_fields,
                                                          text=report_builder_fields.default_multiple_column_text)
                        extra_filter = Q((multiple_column_field, result[multiple_column_field]))

                        self.get_number_field(annotations_type=self.chart_report.axis_value_type,
                                              index=f'{index}_{multiple_index}',
                                              data_attr=data_attr,
                                              table_field=table_field,
                                              fields=fields,
                                              col_type_override=col_type_override,
                                              extra_filter=extra_filter,
                                              title_suffix=suffix,
                                              multiple_index=multiple_index)

                else:
                    self.get_number_field(annotations_type=self.chart_report.axis_value_type,
                                          index=index,
                                          data_attr=data_attr,
                                          table_field=table_field,
                                          fields=fields,
                                          col_type_override=col_type_override)
        return fields

    # noinspection PyUnresolvedReferences
    @staticmethod
    def add_colour_offset(colour, multiple_index):
        if multiple_index > 0:
            offset = 50 * multiple_index
            colour_list = list(int(colour[i:i + 2], 16) for i in (0, 2, 4))
            _, colour_list[0] = divmod(colour_list[0] + offset, 255)
            _, colour_list[1] = divmod(colour_list[1] + offset, 255)
            _, colour_list[2] = divmod(colour_list[2] + offset, 255)
            return "{:02x}{:02x}{:02x}".format(*colour_list)
        else:
            return colour

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_model = self.chart_report.get_base_modal()

        if hasattr(self.chart_report, 'axis_scale'):
            self.table = self.chart_js_table(model=base_model, axis_scale=self.chart_report.axis_scale)
        else:
            self.table = self.chart_js_table(model=base_model)
        self.table.extra_filters = self.extra_filters
        fields = self.process_query_results(base_model=base_model, table=self.table)
        self.table.add_columns(*fields)
        context['show_toolbar'] = self.show_toolbar
        context['datatable'] = self.table
        context['title'] = self.get_title()
        return context

    def setup_menu(self):
        super().setup_menu()
        if not self.show_toolbar:
            return

        if self.dashboard_report and self.enable_edit:
            report_menu = self.pod_dashboard_edit_menu()
        elif self.dashboard_report and not self.enable_edit:
            report_menu = self.pod_dashboard_view_menu()
        else:
            report_menu = self.pod_report_menu()

        self.add_menu('button_menu', 'button_group').add_items(
            *report_menu,
            *self.queries_menu(),
        )

    def pod_dashboard_edit_menu(self):
        return [MenuItem(f'advanced_report_builder:dashboard_report_modal,pk-{self.dashboard_report.id}',
                         menu_display='Edit',
                         font_awesome='fas fa-pencil-alt', css_classes=['btn-primary'])]

    # noinspection PyMethodMayBeStatic
    def pod_dashboard_view_menu(self):
        return []

    def pod_report_menu(self):
        query_id = self.slug.get(f'query{self.chart_report.id}')
        slug_str = ''
        if query_id:
            slug_str = f'-query_id-{query_id}'
        return self.edit_report_menu(chart_report_id=self.chart_report.id, slug_str=slug_str)

    @staticmethod
    def edit_report_menu(chart_report_id, slug_str):
        return []

    # noinspection PyMethodMayBeStatic
    def queries_menu(self):
        return []


class ChartBaseFieldForm(CrispyForm):

    def __init__(self, *args, **kwargs):
        self.django_field = None
        self.col_type_override = None
        super().__init__(*args, **kwargs)

    def submit_button(self, css_class='btn-success modal-submit', button_text='Submit', **kwargs):
        if isinstance(self.django_field, NUMBER_FIELDS):
            return StrictButton(button_text, onclick=f'save_modal_{self.form_id}()', css_class=css_class, **kwargs)
        else:
            return super().submit_button(css_class, button_text, **kwargs)

    def get_report_type_details(self):
        data = json.loads(base64.b64decode(self.slug['data']))

        report_type = get_object_or_404(ReportType, pk=self.slug['report_type_id'])
        base_model = report_type.content_type.model_class()
        self.django_field, self.col_type_override, _ = get_django_field(base_model=base_model, field=data['field'])

        return report_type, base_model

    def _get_query_builder_foreign_key_fields(self, base_model, report_builder_fields, fields,
                                              prefix='', title_prefix='', previous_base_model=None):
        for include in report_builder_fields.includes:
            app_label, model, report_builder_fields_str = include['model'].split('.')
            new_model = apps.get_model(app_label, model)
            if new_model != previous_base_model:
                new_report_builder_fields = getattr(new_model, report_builder_fields_str, None)
                fields.append((prefix + include['field'], title_prefix + include['title']))
                self._get_query_builder_foreign_key_fields(base_model=new_model,
                                                           report_builder_fields=new_report_builder_fields,
                                                           fields=fields,
                                                           prefix=f"{prefix}{include['field']}__",
                                                           title_prefix=f"{title_prefix}{include['title']} --> ",
                                                           previous_base_model=base_model)
