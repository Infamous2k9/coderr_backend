"""Custom pagination allowing the client to control page size."""

from rest_framework.pagination import PageNumberPagination


class OfferPagination(PageNumberPagination):
    """Standard page-number pagination with a client-adjustable page_size."""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
