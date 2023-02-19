from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    DeleteView,
    UpdateView,
    CreateView,
    ListView,
    DetailView,
)

from .forms import SchemaForm, ColumnFormSet
from .models import Dataset, Schema, Column
from .service import generate_csv_file


class CustomLoginView(LoginView):
    """Login"""

    template_name = "login.html"
    form_class = AuthenticationForm


class CustomLogoutView(LogoutView):
    """Logout"""

    next_page = reverse_lazy("login")


class SchemaListView(LoginRequiredMixin, ListView):
    """List of schemes"""

    login_url = "login"
    model = Schema
    template_name = "schema_list.html"
    context_object_name = "schemas"

    def get_queryset(self):
        schemas = Schema.objects.filter(user=self.request.user)
        return schemas


class SchemaDetailView(LoginRequiredMixin, DetailView):
    """Schema details and creating Data Set"""

    login_url = "login"
    model = Schema
    template_name = "schema_detail.html"
    context_object_name = "schema"


class SchemaCreateView(LoginRequiredMixin, CreateView):
    """Create schema"""

    login_url = "login"
    model = Schema
    form_class = SchemaForm
    template_name = "schema_create_update.html"
    success_url = reverse_lazy("schema_list")

    def get_context_data(self, **kwargs):
        formset = ColumnFormSet(queryset=Column.objects.none())
        if self.request.POST:
            kwargs["formset"] = ColumnFormSet(self.request.POST)
        else:
            for i, form in enumerate(formset):
                form.prefix = f"form-{i}"
            kwargs["formset"] = formset
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        if formset.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()

            for column_form in formset.forms:
                if column_form.is_valid():
                    column = column_form.save(commit=False)
                    column.schema = self.object
                    column.save()
            return super().form_valid(form)
        else:
            print(formset.errors)
            return self.form_invalid(form)


class SchemaUpdateView(LoginRequiredMixin, UpdateView):
    """Update schema"""

    login_url = "login"
    model = Schema
    form_class = SchemaForm
    template_name = "schema_create_update.html"
    success_url = reverse_lazy("schema_list")

    def get_context_data(self, **kwargs):
        kwargs["is_update"] = True
        if self.request.POST:
            kwargs["formset"] = ColumnFormSet(
                self.request.POST, queryset=Column.objects.filter(schema=self.object)
            )
        else:
            kwargs["formset"] = ColumnFormSet(
                queryset=Column.objects.filter(schema=self.object)
            )
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        if formset.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()

            for column_form in formset.forms:
                if column_form.is_valid():
                    column = column_form.save(commit=False)
                    column.schema = self.object
                    column.save()
            return super().form_valid(form)
        else:
            print(formset.errors)
            return self.form_invalid(form)


class SchemaDeleteView(LoginRequiredMixin, DeleteView):
    """Delete schema"""

    login_url = "login"
    model = Schema
    success_url = reverse_lazy("schema_list")


@method_decorator(csrf_exempt, name="dispatch")
class DeleteColumnView(LoginRequiredMixin, View):
    """Delete Column on UPDATE page"""

    def delete(self, request, pk):
        if request.method == "DELETE":
            try:
                column = Column.objects.get(id=pk)
                column.delete()
                return JsonResponse({"success": True})
            except Column.DoesNotExist:
                return JsonResponse({"success": False, "error": "Column not found"})
        else:
            return JsonResponse({"success": False, "error": "Invalid request method"})


@method_decorator(csrf_exempt, name="dispatch")
class CreateDataset(LoginRequiredMixin, View):
    """Create Data Set"""

    def post(self, request):
        pk = int(request.POST.get("schemaId"))
        schema = Schema.objects.get(pk=pk)
        dataset = Dataset.objects.create(schema=schema)
        return JsonResponse(
            {
                "success": True,
                "id": dataset.id,
                "created": dataset.created_at,
                "status": dataset.status,
            }
        )


@method_decorator(csrf_exempt, name="dispatch")
class UpdateDatasetStatus(LoginRequiredMixin, View):
    """Update Data Set status"""

    def post(self, request):
        schema_pk = int(request.POST.get("schemaId"))
        rows = int(request.POST.get("inputRows"))
        dataset_pk = int(request.POST.get("datasetId"))
        schema = Schema.objects.get(pk=schema_pk)
        dataset = Dataset.objects.get(pk=dataset_pk)
        if request.user == schema.user:
            generate_csv_file(rows, schema, dataset)
            return JsonResponse(
                {
                    "success": True,
                    "id": dataset.id,
                    "created": dataset.created_at,
                    "status": dataset.status,
                    "csv_file": dataset.csv_file.url,
                }
            )
        return JsonResponse({"success": False})
