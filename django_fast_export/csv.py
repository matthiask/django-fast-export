import csv

from django.http import StreamingHttpResponse
from django.utils.text import capfirst, slugify


__all__ = ["StreamingCSVResponse", "all_verbose_names", "all_values"]


class _Echo:
    def write(self, value):
        return value


class StreamingCSVResponse(StreamingHttpResponse):
    def __init__(
        self,
        rows_iterator,
        /,
        dialect="unix",
        filename="export.csv",
        as_attachment=True,
    ):
        writer = csv.writer(_Echo(), dialect=dialect)
        disposition = "attachment" if as_attachment else "inline"
        super().__init__(
            (writer.writerow(row) for row in rows_iterator),
            content_type="text/csv",
            headers={
                "Content-Disposition": f'{disposition}; filename="{filename}"',
            },
        )

    @classmethod
    def from_queryset(cls, queryset, /):
        filename = f"{slugify(queryset.model._meta.verbose_name_plural)}.csv"

        def generate():
            yield all_verbose_names(queryset.model)
            yield from (all_values(instance) for instance in queryset)

        return cls(generate(), filename=filename)


def all_verbose_names(model):
    return [capfirst(str(field.verbose_name)) for field in model._meta.fields]


def all_values(instance):
    return [getattr(instance, field.name) for field in instance._meta.fields]
