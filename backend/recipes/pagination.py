from rest_framework.pagination import PageNumberPagination
from foodgram.settings import PS


class RecipePagination(PageNumberPagination):
    page_size = PS
    page_size_query_param = "limit"
