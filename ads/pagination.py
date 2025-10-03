from rest_framework.pagination import PageNumberPagination


class StandardResultPagination(PageNumberPagination):
    """
    Пагинация с выводом 4-х объявлений на страницу.
    """
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 10
