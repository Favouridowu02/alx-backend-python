from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    """
    Message Pagination Class - returns 20 messages per page by default.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


# "page.paginator.count"