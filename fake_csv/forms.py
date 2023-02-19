from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Field
from django import forms
from django.forms import modelformset_factory

from .models import Schema, Column


class SchemaForm(forms.ModelForm):
    """Form for creating schema"""

    class Meta:
        model = Schema
        fields = ('name', 'column_separator', 'string_character')

    def __init__(self, *args, **kwargs):
        super(SchemaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'd-flex justify-content-left'
        self.helper.layout = Layout(
            Field('name', css_class='w-50'),
            Field('column_separator', css_class='w-50'),
            Field('string_character', css_class='w-50')
        )


class ColumnForm(forms.ModelForm):
    """Form for creating schema columns"""

    class Meta:
        model = Column
        fields = ('name', 'type', 'from_value', 'to_value', 'order')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_value'].disabled = False
        self.fields['to_value'].disabled = False


ColumnFormSet = modelformset_factory(Column, form=ColumnForm, extra=0)
