from rest_framework.pagination import PageNumberPagination


class LimitPageNumberPagination(PageNumberPagination):
    """Паджинатор с параметром limit."""

    page_size_query_param = "limit"
