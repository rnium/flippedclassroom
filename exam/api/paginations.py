from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class AnswerSheetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'p'
    def get_paginated_response(self, data):
        return  Response({
            'prev': self.get_previous_link(),
            'next': self.get_next_link(),
            'current_page': int(self.get_page_number(self.request, self.page.paginator)),
            'total_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'results': data
        })