==================
django-fast-export
==================


Utilities for quickly streaming CSV responses to the client

Thanks, https://docs.djangoproject.com/en/4.0/howto/outputting-csv/

Example usage:

.. code-block:: python

    from django_fast_export.csv import StreamingCSVResponse

    response = StreamingCSVResponse.from_queryset(queryset)

Or with additional fields:

.. code-block:: python

    from django_fast_export.csv import StreamingCSVResponse, all_values, all_verbose_names

    def generate():
        yield (all_verbose_names(queryset.model) + ["Lösungen"])
        yield from (
            (all_values(instance) + [instance.get_solutions()]) for instance in queryset
        )

    response = StreamingCSVResponse(generate())
