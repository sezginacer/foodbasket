from collections import defaultdict
from typing import Any, Callable, Dict, Generator, Iterable, List, Tuple, TypeVar

from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.views import set_rollback

T = TypeVar("T")


def _groupby(
    iterable: Iterable[T], key: Callable[[T], Any]
) -> Generator[Tuple[Any, List[T]], None, None]:
    # since itertools.groupby surprisingly not worked properly in the case below,
    # wrote a function like that.
    grouped = defaultdict(list)
    for item in iterable:
        grouped[key(item)].append(item)

    for key_, group in grouped.items():
        yield key_, group


def _handle_protected_error(exc: ProtectedError) -> Response:
    groups = []
    for model, objects in _groupby(exc.protected_objects, key=type):
        model_label = model._meta.verbose_name_plural  # noqa
        object_labels = ", ".join(map(str, objects))
        groups.append(f"{model_label} ({object_labels})")

    data = {
        "detail": _("There are some references to the object: {detail}.").format(
            detail=", ".join(groups)
        )
    }
    set_rollback()
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


def exception_handler(exc: Exception, context: Dict) -> Response:
    response = drf_exception_handler(exc, context)

    if response is None and isinstance(exc, ProtectedError):
        response = _handle_protected_error(exc)

    return response
