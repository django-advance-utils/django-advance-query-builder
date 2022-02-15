from django.urls import reverse
from django_modals.modals import ModelFormModal
from django_modals.processes import PROCESS_EDIT_DELETE, PERMISSION_OFF
from django_modals.widgets.colour_picker import ColourPickerWidget

from advanced_report_builder.models import Target
from django.conf import settings


class TargetModal(ModelFormModal):
    model = Target
    form_fields = ['name',
                   'target_type',
                   'colour',
                   'default_value']
    widgets = {'colour': ColourPickerWidget}

    process = PROCESS_EDIT_DELETE
    permission_delete = PERMISSION_OFF

    def post_save(self, created):
        if created:
            url_name = getattr(settings, 'REPORT_BUILDER_TARGET_URL_NAME', '')
            if url_name:
                url = reverse(url_name, kwargs={'slug': self.object.slug})
                self.add_command('redirect', url=url)
