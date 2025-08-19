from __future__ import annotations

import math
from datetime import datetime
from typing import Any
from urllib.parse import urlencode

from litestar import Request, get
from litestar.response import Template
from pony.orm import db_session, select, desc

from ..db.models import Message
from .dto import MessagesQuery


def _query_messages(params: MessagesQuery) -> dict[str, Any]:
    """Fetch messages matching query parameters."""

    query = select(m for m in Message)

    if params.author:
        query = query.filter(lambda m: m.nickname == params.author)
    if params.date_from:
        query = query.filter(lambda m: m.date >= params.date_from)
    if params.date_to:
        query = query.filter(lambda m: m.date <= params.date_to)
    if params.q:
        query = query.filter(lambda m: params.q in m.rank_name)

    sort_fields: list[Any] = []
    for name, order in zip(params.sort, params.order):
        attr = getattr(Message, name, None)
        if not attr:
            continue
        if order == "desc":
            attr = desc(attr)
        sort_fields.append(attr)
    if sort_fields:
        query = query.order_by(*sort_fields)

    total = query.count()
    pages = max(1, math.ceil(total / params.page_size))
    items = query.page(params.page, params.page_size)

    messages = [
        {
            "id": m.id,
            "position": m.position,
            "date": m.date,
            "author": m.nickname,
            "text": m.rank_name,
        }
        for m in items
    ]

    return {
        "messages": messages,
        "total": total,
        "page": params.page,
        "page_size": params.page_size,
        "pages": pages,
        "sort": params.sort,
        "order": params.order,
    }


def _query_string(params: MessagesQuery, **updates: Any) -> str:
    data = params.model_dump(exclude_none=True)
    data.update(updates)
    data["sort"] = ",".join(data.get("sort", []))
    data["order"] = ",".join(data.get("order", []))
    return urlencode(data, doseq=True)


@get("/")
@db_session
def index(request: Request) -> Template:
    """Render the home page."""
    query_data = MessagesQuery(**request.query_params)
    data = _query_messages(query_data)
    base_qs = lambda **kw: _query_string(query_data, **kw)  # noqa: E731
    data.update(
        {
            "position_sort_url": "/partials/messages-table?"
            + base_qs(
                sort=["position", "date"],
                order=[
                    "desc" if query_data.order[0] == "asc" else "asc",
                    query_data.order[1],
                ],
                page=1,
            ),
            "date_sort_url": "/partials/messages-table?"
            + base_qs(
                sort=["position", "date"],
                order=[
                    query_data.order[0],
                    "desc" if query_data.order[1] == "asc" else "asc",
                ],
                page=1,
            ),
            "page_url": lambda p: "/partials/messages-table?" + base_qs(page=p),
        }
    )
    return Template("index.html", context=data)


@get("/partials/messages-table")
@db_session
def messages_table(request: Request) -> Template:
    """Return messages table partial."""
    query_data = MessagesQuery(**request.query_params)
    data = _query_messages(query_data)
    base_qs = lambda **kw: _query_string(query_data, **kw)  # noqa: E731
    data.update(
        {
            "position_sort_url": "/partials/messages-table?"
            + base_qs(
                sort=["position", "date"],
                order=[
                    "desc" if query_data.order[0] == "asc" else "asc",
                    query_data.order[1],
                ],
                page=1,
            ),
            "date_sort_url": "/partials/messages-table?"
            + base_qs(
                sort=["position", "date"],
                order=[
                    query_data.order[0],
                    "desc" if query_data.order[1] == "asc" else "asc",
                ],
                page=1,
            ),
            "page_url": lambda p: "/partials/messages-table?" + base_qs(page=p),
        }
    )
    return Template("_messages_table.html", context=data)


@get("/healthz")
def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
