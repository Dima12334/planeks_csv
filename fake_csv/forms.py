from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Field
from django import forms
from django.forms import formset_factory

from .models import Schema, Column


class SchemaForm(forms.ModelForm):
    """Form for creating schema"""

    class Meta:
        model = Schema
        fields = ('name', 'column_separator', 'string_character')

    def __init__(self, *args, **kwargs):
        self.is_add = kwargs.pop('is_add', False)
        super(SchemaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'd-flex justify-content-left'
        self.helper.layout = Layout(
            'name',
            'column_separator',
            'string_character',
            Submit('submit', 'Add columns' if self.is_add else 'Edit columns', css_class='btn btn-primary')
        )


class ColumnForm(forms.ModelForm):
    """Form for creating schema columns"""

    class Meta:
        model = Column
        fields = ('name', 'type', 'from_value', 'to_value', 'order')

    def __init__(self, *args, **kwargs):
        self.is_add = kwargs.pop('is_add', False)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'd-flex justify-content-left mx-1'
        self.helper.field_class = 'mx-1'
        self.fields['from_value'].disabled = False
        self.fields['to_value'].disabled = False
        self.helper.layout = Layout(
            Row(
                Field('name'),
                Field('type'),
                Field('from_value'),
                Field('to_value'),
                Field('order'),
            ),
            Submit('submit', 'Add column' if self.is_add else 'Edit column', css_class='btn btn-primary')
        )


# class SchemaForm(forms.ModelForm):
#     class Meta:
#         model = Schema
#         fields = ('name', 'column_separator', 'string_character')
#
#         widgets = {
#             'name': forms.TextInput(attrs={'placeholder': 'Name'}),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super(SchemaForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.label_class = 'd-flex justify-content-left'
#         self.helper.layout = Layout(
#             'name',
#             'column_separator',
#             'string_character',
#         )
#
#
# class ColumnForm(forms.ModelForm):
#     class Meta:
#         model = Column
#         fields = ('name', 'type', 'from_value', 'to_value', 'order')
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.label_class = 'd-flex justify-content-left mx-1'
#         self.helper.field_class = 'mx-1'
#         self.fields['from_value'].disabled = False
#         self.fields['to_value'].disabled = False
#         self.helper.layout = Layout(
#             Row(
#                 Field('name'),
#                 Field('type'),
#                 Field('from_value'),
#                 Field('to_value'),
#                 Field('order'),
#             )
#         )
#
#
# ColumnFormSet = formset_factory(
#     ColumnForm,
#     extra=0,
#     min_num=1
# )