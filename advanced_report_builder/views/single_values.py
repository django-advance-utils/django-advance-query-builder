import copy

from ajax_helpers.mixins import AjaxHelpers
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django_datatables.datatables import HorizontalTable
from django_menus.menu import MenuMixin, MenuItem
from django_modals.modals import ModelFormModal
from django_modals.processes import PROCESS_EDIT_DELETE, PERMISSION_OFF
from django_modals.widgets.colour_picker import ColourPickerWidget
from django_modals.widgets.select2 import Select2

from advanced_report_builder.columns import ReportBuilderNumberColumn
from advanced_report_builder.filter_query import FilterQueryMixin
from advanced_report_builder.globals import NUMBER_FIELDS, ANNOTATION_FUNCTIONS, BOOLEAN_FIELD
from advanced_report_builder.models import SingleValueReport, ReportType
from advanced_report_builder.utils import split_slug, get_django_field


class SingleValueView(AjaxHelpers, FilterQueryMixin, MenuMixin, TemplateView):
    number_field = ReportBuilderNumberColumn
    template_name = 'advanced_report_builder/single_value/report.html'

    def __init__(self, *args, **kwargs):
        self.single_value_report = None
        self.show_toolbar = False
        super().__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.slug = split_slug(kwargs.get('slug'))
        self.report = kwargs.get('report')
        self.single_value_report = self.report.singlevaluereport
        self.enable_edit = kwargs.get('enable_edit')
        self.dashboard_report = kwargs.get('dashboard_report')
        if self.enable_edit or (self.dashboard_report and not self.dashboard_report.top) or not self.dashboard_report:
            self.show_toolbar = True
        return super().dispatch(request, *args, **kwargs)

    def extra_filters(self, query):
        report_query = self.get_report_query(report=self.single_value_report)
        if not report_query:
            return query

        return self.process_filters(query=query,
                                    search_filter_data=report_query.query)

    def get_number_field(self, fields, field_name, col_type_override, aggregations_type, decimal_places=0):

        if col_type_override:
            field = copy.deepcopy(col_type_override)
            if aggregations_type == 'count':
                new_field_name = f'{aggregations_type}_{field_name}'
                number_function_kwargs = {}
                function = ANNOTATION_FUNCTIONS[aggregations_type]
                number_function_kwargs['annotations'] = {new_field_name: function(field.field)}

                number_function_kwargs.update({'field': new_field_name,
                                               'column_name': field_name})
                field = self.number_field(**number_function_kwargs)
            else:
                if aggregations_type:
                    new_field_name = f'{aggregations_type}_{field_name}'

                    function = ANNOTATION_FUNCTIONS[aggregations_type]
                    field.aggregations = {new_field_name: function(field.field)}
                    field.field = new_field_name
                    field.options['calculated'] = True

            fields.append(field)
        else:
            number_function_kwargs = {}
            if decimal_places:
                number_function_kwargs = {'decimal_places': int(decimal_places)}

            if aggregations_type:
                new_field_name = f'{aggregations_type}_{field_name}'
                function = ANNOTATION_FUNCTIONS[aggregations_type]
                number_function_kwargs['aggregations'] = {new_field_name: function(field_name)}
                field_name = new_field_name

            number_function_kwargs.update({'field': field_name,
                                           'column_name': field_name,
                                           'options': {'calculated': True},
                                           'model_path': ''})

            field = self.number_field(**number_function_kwargs)
            fields.append(field)

        return field_name

    def _process_aggregations(self, fields, aggregations_type='sum'):
        field = self.single_value_report.field
        base_modal = self.single_value_report.get_base_modal()

        django_field, col_type_override, _ = get_django_field(base_modal=base_modal, field=field)

        if isinstance(django_field, NUMBER_FIELDS) or isinstance(django_field, BOOLEAN_FIELD):
            self.get_number_field(fields=fields,
                                  field_name=field,
                                  col_type_override=col_type_override,
                                  aggregations_type=aggregations_type,
                                  decimal_places=self.single_value_report.decimal_places)
        else:
            assert False, 'not a number field'


    def _get_count(self, fields):

        number_function_kwargs = {'aggregations': {'count': Count(1)},
                                  'field': 'count',
                                  'column_name': 'count',
                                  'options': {'calculated': True},
                                  'model_path': ''}

        field = self.number_field(**number_function_kwargs)
        fields.append(field)

    def process_query_results(self):
        single_value_type = self.single_value_report.single_value_type
        fields = []
        if single_value_type == SingleValueReport.SINGLE_VALUE_TYPE_COUNT:
            self._get_count(fields=fields)
        elif single_value_type == SingleValueReport.SINGLE_VALUE_TYPE_SUM:
            self._process_aggregations(fields=fields, aggregations_type='sum')
        elif single_value_type == SingleValueReport.SINGLE_VALUE_TYPE_COUNT_AND_SUM:
            self._get_count(fields=fields)
            self._process_aggregations(fields=fields, aggregations_type='sum')
        elif single_value_type == SingleValueReport.SINGLE_VALUE_TYPE_AVERAGE:
            self._process_aggregations(fields=fields, aggregations_type='avg')
        elif single_value_type == SingleValueReport.SINGLE_VALUE_TYPE_PERCENT:
            assert False
        return fields

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_modal = self.single_value_report.get_base_modal()

        table = HorizontalTable(model=base_modal)
        table.datatable_template = 'advanced_report_builder/single_value/middle.html'
        table.extra_filters = self.extra_filters
        fields = self.process_query_results()
        table.add_columns(
            *fields
        )
        context['show_toolbar'] = self.show_toolbar
        context['datatable'] = table
        context['single_value_report'] = self.single_value_report
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

    def pod_dashboard_view_menu(self):
        return []

    def pod_report_menu(self):

        query_id = self.slug.get(f'query{self.single_value_report.id}')
        slug_str = ''
        if query_id:
            slug_str = f'-query_id-{query_id}'

        return [MenuItem(f'advanced_report_builder:single_value_modal,pk-{self.single_value_report.id}{slug_str}',
                         menu_display='Edit',
                         font_awesome='fas fa-pencil-alt', css_classes=['btn-primary'])]

    def queries_menu(self):
        return []


class SingleValueModal(ModelFormModal):
    size = 'xl'
    template_name = 'advanced_report_builder/single_value/modal.html'
    process = PROCESS_EDIT_DELETE
    permission_delete = PERMISSION_OFF
    model = SingleValueReport
    widgets = {'tile_colour': ColourPickerWidget}

    form_fields = ['name',
                   'report_type',
                   ('single_value_type', {'label': 'Value type'}),
                   ('numerator', {'label': 'Numerator field'}),
                   'field',
                   'tile_colour',
                   ('decimal_places', {'field_class': 'col-md-5 col-lg-3 input-group-sm'})
                   ]

    def form_setup(self, form, *_args, **_kwargs):
        form.add_trigger('single_value_type', 'onchange', [
            {'selector': '#div_id_field',
             'values': {SingleValueReport.SINGLE_VALUE_TYPE_COUNT: 'hide'},
             'default': 'show'},
            {'selector': '#div_id_numerator',
             'values': {SingleValueReport.SINGLE_VALUE_TYPE_PERCENT: 'show'},
             'default': 'hide'},
            {'selector': 'label[for=id_field]',
             'values': {SingleValueReport.SINGLE_VALUE_TYPE_PERCENT: ('html', 'Denominator field')},
             'default': ('html', 'Dield')},
        ])

        fields = []
        if form.instance.field:

            form.fields['field'].initial = form.instance.field

            base_model = form.instance.report_type.content_type.model_class()
            report_builder_fields = getattr(base_model, form.instance.report_type.report_builder_class_name, None)

            self._get_fields(base_model=base_model,
                             fields=fields,
                             report_builder_fields=report_builder_fields,
                             selected_field_id=form.instance.field)

        form.fields['field'].widget = Select2(attrs={'ajax': True})
        form.fields['field'].widget.select_data = fields

        form.fields['numerator'].widget = Select2(attrs={'ajax': True})
        form.fields['numerator'].widget.select_data = fields

    def select2_field(self, **kwargs):
        fields = []
        if kwargs['report_type'] != '':
            report_type = get_object_or_404(ReportType, pk=kwargs['report_type'])
            base_model = report_type.content_type.model_class()
            report_builder_fields = getattr(base_model, report_type.report_builder_class_name, None)
            fields = []
            self._get_fields(base_model=base_model,
                             fields=fields,
                             report_builder_fields=report_builder_fields)

        return JsonResponse({'results': fields})

    def select2_numerator(self, **kwargs):
        return self.select2_field(**kwargs)

    def _get_fields(self, base_model, fields, report_builder_fields,
                    prefix='', title_prefix='', selected_field_id=None):

        for report_builder_field in report_builder_fields.fields:

            django_field, _, columns = get_django_field(base_modal=base_model, field=report_builder_field)

            for column in columns:
                if isinstance(django_field, NUMBER_FIELDS) or isinstance(django_field, BOOLEAN_FIELD):
                    full_id = prefix + column.column_name
                    if selected_field_id is None or selected_field_id == full_id:
                        fields.append({'id': full_id,
                                       'text': title_prefix + column.title})

        for include in report_builder_fields.includes:
            app_label, model, report_builder_fields_str = include['model'].split('.')
            new_model = apps.get_model(app_label, model)
            new_report_builder_fields = getattr(new_model, report_builder_fields_str, None)
            self._get_fields(base_model=new_model,
                             fields=fields,
                             report_builder_fields=new_report_builder_fields,
                             prefix=f"{include['field']}__",
                             title_prefix=include['title'] + ' -> ')

    def form_valid(self, form):
        single_value_report = form.save()
        single_value_report.save()
        return self.command_response('reload')

    def clean(self, form, cleaned_data):
        if cleaned_data['single_value_type'] != SingleValueReport.SINGLE_VALUE_TYPE_COUNT and not cleaned_data['field']:
            raise ValidationError("Please select a field")
