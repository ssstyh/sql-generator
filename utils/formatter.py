from __future__ import annotations

import sqlparse


class SQLFormatter:
    """Keep generated SQL readable and consistently styled."""

    def format_sql(self, sql: str) -> str:
        formatted = sqlparse.format(
            sql.strip(),
            keyword_case="upper",
            reindent=True,
            indent_width=2,
            strip_comments=False,
        )
        return formatted.strip() + "\n"
