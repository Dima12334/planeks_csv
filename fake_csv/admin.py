from django.contrib import admin
from .models import Schema, Column, Dataset


class ColumnInLine(admin.StackedInline):
    model = Column


class DatasetInLine(admin.StackedInline):
    model = Dataset


@admin.register(Schema)
class SchemaAdmin(admin.ModelAdmin):
    """Admin Schema"""

    inlines = [ColumnInLine, DatasetInLine]
    list_display = [
        "name",
        "column_separator",
        "string_character",
        "modified_at",
        "user",
    ]
    list_display_links = [
        "name",
        "column_separator",
        "string_character",
        "modified_at",
        "user",
    ]
    ordering = ["modified_at"]


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    """Admin Column"""

    list_display = ["schema", "name", "type", "order"]
    list_display_links = ["schema", "name", "type", "order"]
    ordering = ["schema"]


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    """Admin Data Set"""

    list_display = ["schema", "created_at", "status"]
    list_display_links = ["schema", "created_at", "status"]
    ordering = ["created_at"]
