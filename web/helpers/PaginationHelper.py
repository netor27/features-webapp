from flask import url_for
from flask import current_app


class PaginationHelper():
    def __init__(self, request, query, resource_for_url, key_name, schema, order_by=None, paginate_id=None):
        self.request = request
        self.query = query
        self.resource_for_url = resource_for_url
        self.key_name = key_name
        self.schema = schema
        self.page_size_argument_name = current_app.config['PAGINATION_PAGE_SIZE_ARGUMENT_NAME']
        self.page_argument_name = current_app.config['PAGINATION_PAGE_ARGUMENT_NAME']
        self.order_by = order_by
        self.paginate_id = paginate_id

    def paginate_query(self):
        # If no page number is specified, we assume the request wants page #1
        page_number = self.request.args.get(
            self.page_argument_name, 1, type=int)
        results_per_page = self.request.args.get(
            self.page_size_argument_name, 5, type=int)
        paginated_objects = self.query.order_by(self.order_by).paginate(
            page_number,
            per_page=results_per_page,
            error_out=False)
        objects = paginated_objects.items
        if paginated_objects.has_prev:
            previous_page_url = url_for(
                self.resource_for_url,
                page=page_number - 1,
                size=results_per_page,
                id=self.paginate_id,
                _external=True)
        else:
            previous_page_url = None
        if paginated_objects.has_next:
            next_page_url = url_for(
                self.resource_for_url,
                page=page_number + 1,
                size=results_per_page,
                id=self.paginate_id,
                _external=True)
        else:
            next_page_url = None
        dumped_objects = self.schema.dump(objects, many=True).data
        return ({
            self.key_name: dumped_objects,
            'previous': previous_page_url,
            'next': next_page_url,
            'count': paginated_objects.total
        })
