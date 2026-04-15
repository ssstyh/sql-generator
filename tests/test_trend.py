import pytest

from core import GenerationRequest, SQLGenerator


@pytest.mark.parametrize(
    ("dialect", "granularity", "expected_fragment"),
    [
        ("mysql", "day", "DATE(order_date) AS period_start"),
        (
            "mysql",
            "week",
            "DATE_SUB(DATE(order_date), INTERVAL WEEKDAY(order_date) DAY) AS period_start",
        ),
        (
            "mysql",
            "month",
            "DATE_SUB(DATE(order_date), INTERVAL DAYOFMONTH(order_date) - 1 DAY) AS period_start",
        ),
        ("postgresql", "day", "DATE_TRUNC('day', order_date)::date AS period_start"),
        ("postgresql", "week", "DATE_TRUNC('week', order_date)::date AS period_start"),
        ("postgresql", "month", "DATE_TRUNC('month', order_date)::date AS period_start"),
    ],
)
def test_trend_sql_supports_expected_granularity(
    dialect: str,
    granularity: str,
    expected_fragment: str,
) -> None:
    generator = SQLGenerator()

    sql = generator.generate(
        GenerationRequest(
            analysis_type="trend",
            dialect=dialect,
            parameters={
                "table_name": "user_orders",
                "date_field": "order_date",
                "metric_field": "amount",
                "aggregation": "sum",
                "granularity": granularity,
            },
        )
    )

    assert expected_fragment.upper() in sql.upper()
    assert "METRIC_VALUE" in sql.upper()


@pytest.mark.parametrize(
    ("aggregation", "expected_fragment"),
    [
        ("sum", "SUM(METRIC_VALUE_SOURCE) AS METRIC_VALUE"),
        ("count", "COUNT(*) AS METRIC_VALUE"),
        ("count_distinct", "COUNT(DISTINCT METRIC_VALUE_SOURCE) AS METRIC_VALUE"),
    ],
)
def test_trend_sql_supports_primary_aggregations(aggregation: str, expected_fragment: str) -> None:
    generator = SQLGenerator()

    sql = generator.generate(
        GenerationRequest(
            analysis_type="trend",
            dialect="mysql",
            parameters={
                "table_name": "user_orders",
                "date_field": "order_date",
                "metric_field": "amount",
                "aggregation": aggregation,
                "granularity": "day",
            },
        )
    )

    assert expected_fragment.upper() in sql.upper()


def test_compare_sql_supports_mom_output_structure() -> None:
    generator = SQLGenerator()

    sql = generator.generate(
        GenerationRequest(
            analysis_type="compare",
            dialect="mysql",
            parameters={
                "table_name": "user_orders",
                "date_field": "order_date",
                "metric_field": "amount",
                "aggregation": "sum",
                "granularity": "month",
                "comparison_type": "mom",
                "date_range": {"start": "2026-01-01", "end": "2026-03-31"},
            },
        )
    )

    sql_upper = sql.upper()
    assert "LAG(METRIC_VALUE) OVER" in sql_upper
    assert "CURRENT_VALUE" in sql_upper
    assert "PREVIOUS_VALUE" in sql_upper
    assert "CHANGE_RATE" in sql_upper


def test_compare_sql_supports_yoy_output_structure() -> None:
    generator = SQLGenerator()

    sql = generator.generate(
        GenerationRequest(
            analysis_type="compare",
            dialect="postgresql",
            parameters={
                "table_name": "user_orders",
                "date_field": "order_date",
                "metric_field": "amount",
                "aggregation": "count",
                "granularity": "week",
                "comparison_type": "yoy",
                "filter_conditions": [
                    {"field": "channel", "operator": "=", "value": "app"},
                ],
            },
        )
    )

    sql_upper = sql.upper()
    assert "LEFT JOIN BASE_SERIES PREV" in sql_upper
    assert "INTERVAL '1 YEAR'" in sql_upper
    assert "COUNT(*) AS METRIC_VALUE" in sql_upper
    assert "CHANNEL = 'APP'" in sql_upper
