from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination


class Paginator(PageNumberPagination):
    """Custom paginator"""

    def get_paginated_response(self, data):
        return OrderedDict([
            ("pageCount", len(self.page.object_list)),
            ('dataCount', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])
