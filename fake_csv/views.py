from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, UpdateView, CreateView, ListView, DetailView

from .forms import ColumnForm, SchemaForm  # ColumnFormSet
from .models import Dataset, Schema, Column
from .service import generate_csv_file


class CustomLoginView(LoginView):
    """Login"""
    template_name = 'login.html'
    form_class = AuthenticationForm


class CustomLogoutView(LogoutView):
    """Logout"""
    next_page = reverse_lazy('login')


class SchemaListView(LoginRequiredMixin, ListView):
    """List of schemes"""
    login_url = 'login'
    model = Schema
    template_name = 'schema_list.html'
    context_object_name = 'schemas'

    def get_queryset(self):
        schemas = Schema.objects.filter(user=self.request.user)
        return schemas


class SchemaDetailView(LoginRequiredMixin, DetailView):
    """Schema details and creating Data Set"""
    login_url = 'login'
    model = Schema
    template_name = 'schema_detail.html'
    context_object_name = 'schema'


class SchemaCreateView(LoginRequiredMixin, CreateView):
    """Create schema"""
    login_url = 'login'
    model = Schema
    form_class = SchemaForm
    template_name = 'schema_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_add'] = True
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SchemaCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('add_columns', kwargs={'id_schema': self.object.id})


class SchemaUpdateView(LoginRequiredMixin, UpdateView):
    """Update schema"""
    login_url = 'login'
    model = Schema
    form_class = SchemaForm
    template_name = 'schema_update.html'

    def get_context_data(self, **kwargs):
        columns = Column.objects.filter(schema=self.object).order_by('order')
        context = super(SchemaUpdateView, self).get_context_data(**kwargs)
        context['columns'] = columns
        return context

    def get_success_url(self):
        return reverse_lazy('add_columns', kwargs={'id_schema': self.object.id})


class SchemaDeleteView(LoginRequiredMixin, DeleteView):
    """Delete schema"""
    login_url = 'login'
    model = Schema
    success_url = reverse_lazy('schema_list')


# class SchemaCreateView(LoginRequiredMixin, View):
#     login_url = 'login'
#
#     def get(self, request):
#         return render(request, 'create_schema.html', context={
#             'form': SchemaForm(),
#             'formset': ColumnFormSet()
#         })
#
#     def post(self, request):
#         schema_form = SchemaForm(request.POST)
#         formset = ColumnFormSet(request.POST)
#
#         if schema_form.is_valid() and formset.is_valid():
#             schema_data = schema_form.cleaned_data
#             columns_data = formset.cleaned_data
#             new_schema = Schema.objects.create(name=schema_data['name'], user=request.user)
#             new_schema.save()
#
#             for column in columns_data:
#                 new_column = Column.objects.create(schema=new_schema,
#                                     name=column['name'],
#                                     type=column['type'],
#                                     order=column['order'],
#                                     from_value=column['from_value'],
#                                     to_value=column['to_value'])
#                 new_column.save()
#             return redirect('schema_list')
#
#
# class SchemaUpdateView(LoginRequiredMixin, View):
#     login_url = 'login'
#
#     def get(self, request, pk):
#         schema_to_edit = Schema.objects.get(id=pk)
#         columns = Column.objects.filter(schema=schema_to_edit)
#         schema_form = SchemaForm(initial=model_to_dict(schema_to_edit))
#         Formset = forms.modelformset_factory(Column, extra=0, fields=['id', 'name', 'type',
#                                                                       'from_value', 'to_value', 'order'])
#         formset = Formset(initial=[{'id': x.id} for x in schema_to_edit.columns.all()],
#                           queryset=columns)
#         return render(request, 'create_schema.html', context={'schema_form': schema_form, 'formset': formset})
#
#     def post(self, request, pk):
#         schema_to_edit = Schema.objects.get(id=pk)
#         if request.method == 'POST':
#             schema_form = SchemaForm(request.POST, instance=schema_to_edit)
#             formset = ColumnFormSet(request.POST, initial=[x for x in schema_to_edit.columns.all()])
#             if schema_form.is_valid() and formset.is_valid():
#                 schema_form.save()
#
#                 columns_data = formset.cleaned_data
#                 for column in columns_data:
#                     edit_column = Column(schema=schema_to_edit,
#                                         name=column['name'],
#                                         type=column['type'],
#                                         order=column['order'],
#                                         from_value=column.get('from_value'),
#                                         to_value=column.get('to_value'))
#                     edit_column.save()
#                 return redirect('schema_list')
#             else:
#                 print(formset.errors)
#
# def edit_schema(request, pk):
#     schema_to_edit = Schema.objects.get(id=pk)
#     columns = Column.objects.filter(schema=schema_to_edit)
#     schema_form = SchemaForm(initial=model_to_dict(schema_to_edit))
#     Formset = forms.modelformset_factory(Column, extra=0, fields=['id', 'name', 'type',
#                                                                   'from_value','to_value', 'order'])
#     formset = Formset(initial=[{'id': x.id} for x in schema_to_edit.columns.all()],
#                       queryset=columns)
#     if request.method == 'POST':
#         schema_form = SchemaForm(request.POST, instance=schema_to_edit)
#         formset = ColumnFormSet(request.POST)
#         if schema_form.is_valid() and formset.is_valid():
#             schema_form.save()
#
#             columns_data = formset.cleaned_data
#             print(columns_data)
#             for column in columns_data:
#                 edit_column = Column(schema=schema_to_edit,
#                                      name=column['name'],
#                                      type=column['type'],
#                                      order=column['order'],
#                                      from_value=column.get('from_value'),
#                                      to_value=column.get('to_value'))
#                 edit_column.save()
#             return redirect('schema_list')
#         else:
#             print(formset.errors)
#     return render(request, "create_schema.html", {'schema_form': schema_form, 'formset': formset})



class ColumnCreateView(LoginRequiredMixin, CreateView):
    """Create schema columns"""
    login_url = 'login'
    model = Column
    form_class = ColumnForm
    template_name = 'column_create.html'

    def get_success_url(self):
        return reverse_lazy('add_columns', kwargs={'id_schema': self.kwargs['id_schema']})

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.schema = Schema.objects.get(pk=self.kwargs['id_schema'])
        obj.save()
        return super(ColumnCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        schema = Schema.objects.get(pk=self.kwargs['id_schema'])
        columns = Column.objects.filter(schema=schema).order_by('order')
        context = super(ColumnCreateView, self).get_context_data(**kwargs)
        context['columns'] = columns
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_add'] = True
        return kwargs


class ColumnUpdateView(LoginRequiredMixin, UpdateView):
    """Update schema columns"""
    login_url = 'login'
    model = Column
    form_class = ColumnForm
    template_name = 'column_update.html'

    def get_success_url(self):
        schema = Schema.objects.filter(columns__id=self.object.id).first()
        return reverse_lazy('add_columns', kwargs={'id_schema': schema.id})


class ColumnDeleteView(LoginRequiredMixin, DeleteView):
    """Delete schema columns"""
    login_url = 'login'
    model = Column

    def get_success_url(self):
        schema = Schema.objects.filter(columns__id=self.object.id).first()
        return reverse_lazy('add_columns', kwargs={'id_schema': schema.id})


@method_decorator(csrf_exempt, name='dispatch')
class CreateDatasets(LoginRequiredMixin, View):
    """Create Data Set"""

    def post(self, request):
        pk = int(request.POST.get('schemaId'))
        rows = int(request.POST.get('input-rows'))
        schema = Schema.objects.get(pk=pk)
        dataset = Dataset.objects.create(schema=schema)
        if request.user == schema.user:
            generate_csv_file(rows, schema, dataset)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})
        # return HttpResponseRedirect(reverse_lazy('detail_schema', kwargs={'pk': pk}))


@login_required
def check_status(request):
    """Update Data Set status"""

    if request.method == 'GET':
        parameters_dict = dict(request.GET.lists())
        data = []
        if not parameters_dict:
            return JsonResponse(data, safe=False)
        all_dataset_id = parameters_dict['all_dataset_id[]']
        for dataset_id in all_dataset_id:
            dataset = Dataset.objects.get(id=int(dataset_id))
            data_dataset_id = {
                'dataset_id': dataset_id,
                'dataset_status': dataset.status
            }
            if dataset.status == 'Ready':
                data_dataset_id['csv_file'] = str(dataset.csv_file)
            data.append(data_dataset_id)
        return JsonResponse(data, safe=False)
