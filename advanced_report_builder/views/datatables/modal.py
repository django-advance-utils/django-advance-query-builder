import base64
import json

from crispy_forms.bootstrap import StrictButton
from crispy_forms.layout import Div
from django.conf import settings
from django.forms import CharField, ChoiceField, BooleanField, IntegerField
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django_modals.fields import FieldEx
from django_modals.modals import FormModal
from django_modals.processes import PROCESS_EDIT_DELETE, PERMISSION_OFF
from django_modals.widgets.select2 import Select2Multiple, Select2
from django_modals.widgets.widgets import Toggle

from advanced_report_builder.globals import DATE_FIELDS, NUMBER_FIELDS, ANNOTATION_VALUE_CHOICES, ANNOTATIONS_CHOICES, \
    DATE_FORMAT_TYPES, CURRENCY_COLUMNS, LINK_COLUMNS
from advanced_report_builder.models import TableReport, ReportQuery, ReportType
from advanced_report_builder.toggle import RBToggle
from advanced_report_builder.utils import split_attr, get_django_field, encode_attribute, decode_attribute
from advanced_report_builder.views.charts_base import ChartBaseFieldForm
from advanced_report_builder.views.modals_base import QueryBuilderModalBaseMixin, QueryBuilderModalBase


class TableModal(QueryBuilderModalBase):
    template_name = 'advanced_report_builder/datatables/modal.html'
    size = 'xl'
    model = TableReport
    process = PROCESS_EDIT_DELETE
    permission_delete = PERMISSION_OFF

    widgets = {'report_tags': Select2Multiple}

    form_fields = ['name',
                   'notes',
                   ('has_clickable_rows', {'widget': Toggle(attrs={'data-onstyle': 'success',
                                                                   'data-on': 'YES',
                                                                   'data-off': 'NO'})}),
                   'link_field',
                   'page_length',
                   'report_type',
                   'report_tags',
                   'table_fields',
                   'pivot_fields',
                   ]

    def __init__(self, *args, **kwargs):
        self.report_query = None
        self.show_query_name = False
        super().__init__(*args, **kwargs)

    def form_setup(self, form, *_args, **_kwargs):
        self.add_query_data(form)
        url = reverse('advanced_report_builder:table_field_modal',
                      kwargs={'slug': 'selector-99999-data-FIELD_INFO-report_type_id-REPORT_TYPE_ID'})

        pivot_url = reverse('advanced_report_builder:table_pivot_modal',
                            kwargs={'slug': 'selector-99999-data-FIELD_INFO-report_type_id-REPORT_TYPE_ID'})

        form.add_trigger('has_clickable_rows', 'onchange', [
            {'selector': '#div_id_link_field', 'values': {'checked': 'show'}, 'default': 'hide'},
        ])

        form.fields['notes'].widget.attrs['rows'] = 3

        link_fields = []

        if 'data' in _kwargs:
            link_field = _kwargs['data'].get('link_field')
            report_type_id = _kwargs['data'].get('report_type')
            report_type = get_object_or_404(ReportType, id=report_type_id)
        else:
            link_field = form.instance.link_field
            report_type = form.instance.report_type
        if link_field:
            form.fields['link_field'].initial = link_field
            base_model = report_type.content_type.model_class()
            report_builder_fields = getattr(base_model, report_type.report_builder_class_name, None)
            self._get_column_link_fields(base_model=base_model,
                                         fields=link_fields,
                                         report_builder_class=report_builder_fields,
                                         selected_field_id=link_field)

        form.fields['link_field'].widget = Select2(attrs={'ajax': True})
        form.fields['link_field'].widget.select_data = link_fields

        fields = ['name',
                  'notes',
                  'report_type',
                  'report_tags',
                  FieldEx('has_clickable_rows', template='django_modals/fields/label_checkbox.html'),
                  'link_field',
                  FieldEx('page_length', template='django_modals/fields/label_checkbox.html'),
                  FieldEx('table_fields',
                          template='advanced_report_builder/select_column.html',
                          extra_context={'select_column_url': url}),
                  FieldEx('pivot_fields',
                          template='advanced_report_builder/datatables/select_pivot.html',
                          extra_context={'select_column_url': pivot_url}),
                  ]

        if self.show_query_name:
            fields.append(FieldEx('query_name'))

        fields.append(FieldEx('query_data', template='advanced_report_builder/query_builder.html'))
        return fields

    def form_valid(self, form):
        org_id = self.object.id if hasattr(self, 'object') else None
        table_report = form.save()

        if not self.report_query and form.cleaned_data['query_data']:
            query = form.cleaned_data['query_data']
            ReportQuery(query=query,
                        report=table_report).save()
        elif form.cleaned_data['query_data']:
            self.report_query.query = form.cleaned_data['query_data']
            if self.show_query_name:
                self.report_query.name = form.cleaned_data['query_name']
            self.report_query.save()
        elif self.report_query:
            self.report_query.delete()
        url_name = getattr(settings, 'REPORT_BUILDER_DETAIL_URL_NAME', '')
        if org_id is None and url_name:
            url = reverse(url_name, kwargs={'slug': table_report.slug})
            return self.command_response('redirect', url=url)
        else:
            return self.command_response('reload')

    def ajax_get_fields(self, **kwargs):
        report_type_id = kwargs['report_type']
        report_builder_class, base_model = self.get_report_builder_class(report_type_id=report_type_id)
        fields = []
        tables = []
        pivot_fields = []
        self._get_fields(base_model=base_model,
                         fields=fields,
                         tables=tables,
                         report_builder_class=report_builder_class,
                         pivot_fields=pivot_fields)

        self.add_command('report_fields', data=json.dumps({'fields': fields, 'tables': tables}))
        self.add_command('report_pivots', data=json.dumps({'pivot_fields': pivot_fields}))

        return self.command_response()

    def select2_link_field(self, **kwargs):
        fields = []
        if kwargs['report_type'] != '':
            report_builder_fields, base_model = self.get_report_builder_class(report_type_id=kwargs['report_type'])
            fields = []
            self._get_column_link_fields(base_model=base_model,
                                         fields=fields,
                                         report_builder_class=report_builder_fields,
                                         search_string=kwargs.get('search'))

        return JsonResponse({'results': fields})


class TableFieldForm(ChartBaseFieldForm):

    def submit_button(self, css_class='btn-success modal-submit', button_text='Submit', **kwargs):
        if self.django_field is not None and isinstance(self.django_field, NUMBER_FIELDS):
            return StrictButton(button_text, onclick=f'save_modal_{self.form_id}()', css_class=css_class, **kwargs)
        else:
            return super().submit_button(css_class, button_text, **kwargs)

    def setup_modal(self, *args, **kwargs):
        data = json.loads(base64.b64decode(self.slug['data']))
        report_type, base_model = self.get_report_type_details()

        self.fields['title'] = CharField(initial=data['title'])

        data_attr = split_attr(data)
        if self.django_field is not None and isinstance(self.django_field, DATE_FIELDS):
            self.fields['annotations_value'] = ChoiceField(choices=[(0, '-----')] + ANNOTATION_VALUE_CHOICES,
                                                           required=False)
            if 'annotations_value' in data_attr:
                self.fields['annotations_value'].initial = data_attr['annotations_value']
            self.fields['date_format'] = ChoiceField(choices=[(0, '-----')] + DATE_FORMAT_TYPES, required=False)
            if 'date_format' in data_attr:
                self.fields['date_format'].initial = data_attr['date_format']
        elif self.django_field is not None and isinstance(self.django_field, NUMBER_FIELDS):
            self.fields['annotations_type'] = ChoiceField(choices=[(0, '-----')] + ANNOTATIONS_CHOICES,
                                                          required=False)
            if 'annotations_type' in data_attr:
                self.fields['annotations_type'].initial = data_attr['annotations_type']
            self.fields['show_totals'] = BooleanField(required=False, widget=RBToggle())
            if 'show_totals' in data_attr and data_attr['show_totals'] == '1':
                self.fields['show_totals'].initial = True
            self.fields['decimal_places'] = IntegerField()
            self.fields['decimal_places'].initial = int(data_attr.get('decimal_places', 0))
            self.fields['has_filter'] = BooleanField(required=False, widget=RBToggle())

            self.fields['filter'] = CharField(required=False)

            if data_attr.get('has_filter') == '1':
                self.fields['has_filter'].initial = True
                if 'filter' in data_attr:
                    self.fields['filter'].initial = decode_attribute(data_attr['filter'])

            self.fields['multiple_columns'] = BooleanField(required=False, widget=RBToggle())

            report_builder_fields = getattr(base_model, report_type.report_builder_class_name, None)
            fields = []
            self._get_query_builder_foreign_key_fields(base_model=base_model,
                                                       report_builder_fields=report_builder_fields,
                                                       fields=fields)

            self.fields['multiple_column_field'] = ChoiceField(choices=fields, required=False)

            if data_attr.get('multiple_columns') == '1':
                self.fields['multiple_columns'].initial = True
                self.fields['multiple_column_field'].initial = data_attr.get('multiple_column_field')
        elif isinstance(self.col_type_override, CURRENCY_COLUMNS):
            self.fields['show_totals'] = BooleanField(required=False, widget=RBToggle())
            if 'show_totals' in data_attr and data_attr['show_totals'] == '1':
                self.fields['show_totals'].initial = True
        elif isinstance(self.col_type_override, LINK_COLUMNS):
            self.fields['link_html'] = CharField(required=False)
            if 'link_html' in data_attr:
                self.fields['link_html'].initial = decode_attribute(data_attr['link_html'])
            self.fields['link_css'] = CharField(required=False)
            if 'link_css' in data_attr:
                self.fields['link_css'].initial = decode_attribute(data_attr['link_css'])
            self.fields['is_icon'] = BooleanField(required=False, widget=RBToggle())
            if 'is_icon' in data_attr and data_attr['is_icon'] == '1':
                self.fields['is_icon'].initial = True

        super().setup_modal(*args, **kwargs)

    def get_additional_attributes(self):
        attributes = []
        self.get_report_type_details()
        if self.django_field is not None and isinstance(self.django_field, DATE_FIELDS):
            if self.cleaned_data['annotations_value']:
                attributes.append(f'annotations_value-{self.cleaned_data["annotations_value"]}')
            if self.cleaned_data['date_format']:
                attributes.append(f'date_format-{self.cleaned_data["date_format"]}')
        elif self.django_field is not None and isinstance(self.django_field, NUMBER_FIELDS):
            if int(self.cleaned_data['annotations_type']) != 0:
                attributes.append(f'annotations_type-{self.cleaned_data["annotations_type"]}')
            if self.cleaned_data['show_totals'] and self.cleaned_data["show_totals"]:
                attributes.append('show_totals-1')
            if self.cleaned_data['decimal_places'] > 0:
                attributes.append(f'decimal_places-{self.cleaned_data["decimal_places"]}')
            if self.cleaned_data['has_filter']:
                attributes.append(f'has_filter-1')
                if self.cleaned_data['filter']:
                    b64_filter = encode_attribute(self.cleaned_data['filter'])
                    attributes.append(f'filter-{b64_filter}')
                if self.cleaned_data['multiple_columns']:
                    attributes.append('multiple_columns-1')
                    attributes.append(f'multiple_column_field-{self.cleaned_data["multiple_column_field"]}')
        elif isinstance(self.col_type_override, CURRENCY_COLUMNS):
            if self.cleaned_data['show_totals'] and self.cleaned_data["show_totals"]:
                attributes.append('show_totals-1')
        elif isinstance(self.col_type_override, LINK_COLUMNS):
            if self.cleaned_data['link_css']:
                b64_link_css = encode_attribute(self.cleaned_data['link_css'])
                attributes.append(f'link_css-{b64_link_css}')
            if self.cleaned_data['link_html']:
                b64_link_html = encode_attribute(self.cleaned_data['link_html'])
                attributes.append(f'link_html-{b64_link_html}')
            if self.cleaned_data['is_icon'] and self.cleaned_data["is_icon"]:
                attributes.append('is_icon-1')

        if attributes:
            return '-'.join(attributes)
        return None


class TableFieldModal(QueryBuilderModalBaseMixin, FormModal):
    form_class = TableFieldForm
    size = 'xl'
    template_name = 'advanced_report_builder/datatables/fields/modal.html'

    @property
    def modal_title(self):
        data = json.loads(base64.b64decode(self.slug['data']))
        return f'Edit {data["title"]}'

    def form_valid(self, form):
        selector = self.slug['selector']

        _attr = form.get_additional_attributes()
        self.add_command({'function': 'set_attr',
                          'selector': f'#{selector}',
                          'attr': 'data-attr',
                          'val': _attr})

        self.add_command({'function': 'html', 'selector': f'#{selector} span', 'html': form.cleaned_data['title']})
        self.add_command({'function': 'save_query_builder_id_query_data'})
        self.add_command({'function': 'update_selection'})
        return self.command_response('close')

    def form_setup(self, form, *_args, **_kwargs):

        data = json.loads(base64.b64decode(self.slug['data']))
        report_builder_fields, base_model = self.get_report_builder_class(report_type_id=self.slug['report_type_id'])
        django_field, col_type_override, _ = get_django_field(base_model=base_model, field=data['field'])
        if django_field is not None and isinstance(django_field, NUMBER_FIELDS):
            form.add_trigger('annotations_type', 'onchange', [
                {'selector': '#annotations_fields_div', 'values': {'': 'hide'}, 'default': 'show'}])

            form.add_trigger('has_filter', 'onchange', [
                {'selector': '#filter_fields_div', 'values': {'checked': 'show'}, 'default': 'hide'}])

            form.add_trigger('multiple_columns', 'onchange', [
                {'selector': '#multiple_columns_fields_div', 'values': {'checked': 'show'}, 'default': 'hide'},
            ])

            return ['title',
                    'annotations_type',
                    'show_totals',
                    'decimal_places',
                    Div(FieldEx('has_filter',
                                template='django_modals/fields/label_checkbox.html',
                                field_class='col-6 input-group-sm'),
                        Div(
                            FieldEx('filter',
                                    template='advanced_report_builder/datatables/fields/single_query_builder.html'),
                            FieldEx('multiple_columns',
                                    template='django_modals/fields/label_checkbox.html',
                                    field_class='col-6 input-group-sm'),
                            Div(
                                FieldEx('multiple_column_field'),
                                css_id='multiple_columns_fields_div'),
                            css_id='filter_fields_div'),
                        css_id='annotations_fields_div')
                    ]
        elif isinstance(col_type_override, CURRENCY_COLUMNS):
            return ['title',
                    'show_totals']
        elif isinstance(col_type_override, LINK_COLUMNS):
            return ['title',
                    'link_css',
                    'link_html',
                    'is_icon']

    def ajax_get_query_builder_fields(self, **kwargs):
        field_auto_id = kwargs['field_auto_id']

        report_type_id = self.slug['report_type_id']
        query_builder_filters = self.get_query_builder_report_type_field(report_type_id=report_type_id)

        return self.command_response(f'query_builder_{field_auto_id}', data=json.dumps(query_builder_filters))


class TablePivotForm(ChartBaseFieldForm):
    def setup_modal(self, *args, **kwargs):
        data = json.loads(base64.b64decode(self.slug['data']))
        self.fields['title'] = CharField(initial=data['title'])
        super().setup_modal(*args, **kwargs)


class TablePivotModal(QueryBuilderModalBaseMixin, FormModal):
    form_class = TablePivotForm
    size = 'xl'

    @property
    def modal_title(self):
        data = json.loads(base64.b64decode(self.slug['data']))
        return f'Edit {data["title"]}'

    def form_valid(self, form):
        selector = self.slug['selector']

        self.add_command({'function': 'html', 'selector': f'#{selector} span', 'html': form.cleaned_data['title']})
        self.add_command({'function': 'save_query_builder_id_query_data'})
        self.add_command({'function': 'update_pivot_selection'})
        return self.command_response('close')
