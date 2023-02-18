from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Schema(models.Model):
    """Schema model"""

    class ColumnSeparator(models.TextChoices):
        COMMA = ',', 'Comma(,)'
        SEMICOLON = ';', 'Semicolon(;)'

    class StringCharacter(models.TextChoices):
        DOUBLE_QUOTE = '"', 'Double-quote(")'
        SINGLE_QUOTE = "'", "Single-quote(')"

    name = models.CharField(max_length=255, verbose_name='Name')
    column_separator = models.CharField(max_length=50, verbose_name='Column separator', choices=ColumnSeparator.choices,
                                        default=ColumnSeparator.COMMA)
    string_character = models.CharField(max_length=50, verbose_name='String character', choices=StringCharacter.choices,
                                        default=StringCharacter.DOUBLE_QUOTE)
    modified_at = models.DateField(auto_now=True, verbose_name='Modified')
    user = models.ForeignKey(User, verbose_name='Schema author', on_delete=models.CASCADE, related_name='users')

    class Meta:
        verbose_name = 'Schema'
        verbose_name_plural = 'Schemas'

    def __str__(self):
        return f'Schema {self.name}'

    def get_url(self):
        return reverse('detail_schema', args=(self.id,))


class Column(models.Model):
    """Schema Columns model"""

    class ColumnType(models.TextChoices):
        FULL_NAME = 'Full name', 'Full name'
        JOB = 'Job', 'Job'
        EMAIL = 'Email', 'Email'
        PHONE_NUMBER = 'Phone number', 'Phone number'
        INTEGER = 'Integer', 'Integer'
        DATE = 'Date', 'Date'

    schema = models.ForeignKey(Schema, verbose_name='Schema', on_delete=models.CASCADE, related_name='columns')
    name = models.CharField(max_length=255, verbose_name='Column name')
    type = models.CharField(max_length=50, verbose_name='Type', choices=ColumnType.choices,
                            default=ColumnType.FULL_NAME)
    from_value = models.IntegerField(verbose_name='From', null=True, blank=True)
    to_value = models.IntegerField(verbose_name='To', null=True, blank=True)
    order = models.PositiveIntegerField(verbose_name='Order')

    class Meta:
        verbose_name = 'Column'
        verbose_name_plural = 'Columns'

    def __str__(self):
        return f'-{self.name}- column in -{self.schema}- schema'


class Dataset(models.Model):
    """Model for storage Data sets"""

    class Status(models.TextChoices):
        PROCESSING = 'Processing', 'Processing'
        READY = 'Ready', 'Ready'

    schema = models.ForeignKey(Schema, verbose_name='Schema', on_delete=models.CASCADE, related_name='datasets')
    created_at = models.DateField(auto_now_add=True, verbose_name='Created')
    csv_file = models.FileField(verbose_name='CSV file', blank=True, null=True)
    status = models.CharField(max_length=50, verbose_name='Status', choices=Status.choices,
                              default=Status.PROCESSING)

    class Meta:
        verbose_name = 'Dataset'
        verbose_name_plural = 'Datasets'

    def __str__(self):
        return f"{self.schema.user}'s dataset ({self.created_at})"
