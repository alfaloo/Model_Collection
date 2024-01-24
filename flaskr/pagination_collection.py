import os
from flask_paginate import Pagination

class PaginationCollection:
    def __init__(self, builder, page):
        per_page = int(os.getenv("PER_PAGE"))
        offset = (page - 1) * per_page
        total = builder.count()
        self.items = builder.offset(offset).limit(per_page).all()
        self.pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')