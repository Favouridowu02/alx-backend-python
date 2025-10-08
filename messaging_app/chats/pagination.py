import PageNumberPagination from rest_framework.pagination

class MessagePagination(PageNumberPagination):
    """
        Message Pagination Class
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
