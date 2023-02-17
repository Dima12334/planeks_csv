import csv
from datetime import datetime
from faker import Faker

from .models import Column, Dataset

faker = Faker()


def get_fake_data(column_type, from_value=None, to_value=None):
    """Generate fake data"""

    if column_type == 'Full name':
        return faker.name()
    if column_type == 'Job':
        return faker.job()
    if column_type == 'Email':
        return faker.email()
    if column_type == 'Phone number':
        return faker.phone_number()
    if column_type == 'Integer':
        if from_value and to_value:
            return faker.pyint(min_value=min(from_value, to_value), max_value=max(from_value, to_value))
        if from_value:
            return faker.pyint(min_value=from_value, max_value=100)
        if to_value:
            return faker.pyint(min_value=0, max_value=to_value)
        return faker.random_int()
    if column_type == 'Date':
        return faker.date()


def generate_csv_file(count_rows, schema, dataset):
    """Generate CSV file"""

    columns = Column.objects.filter(schema=schema).order_by('order')

    columns_names = [column.name for column in columns]
    delimiter = schema.column_separator
    quote_char = schema.string_character
    filename = f'Dataset_{schema.name}_{datetime.now().strftime("%Y.%m.%d_%H.%M")}.csv'

    with open('media/' + filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, quotechar=quote_char, quoting=csv.QUOTE_NONNUMERIC, delimiter=delimiter)
        writer.writerow(columns_names)
        for _ in range(count_rows):
            fake_data = []
            for column in columns:
                fake_data.append(get_fake_data(column.type, column.from_value, column.to_value))
            writer.writerow(fake_data)

    dataset.csv_file = filename
    dataset.status = Dataset.Status.READY
    dataset.save()
    return
