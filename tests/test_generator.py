from core import GenerationRequest, SQLGenerator


def test_generator_lists_all_expected_analyses() -> None:
    generator = SQLGenerator()

    assert generator.list_supported_analyses() == [
        "compare",
        "funnel",
        "retention",
        "rfm",
        "trend",
    ]


def test_generator_renders_trend_template() -> None:
    generator = SQLGenerator()
    sql = generator.generate(
        GenerationRequest(
            analysis_type="trend",
            dialect="mysql",
            parameters={
                "table_name": "user_orders",
                "date_field": "order_date",
                "metric_field": "amount",
                "aggregation": "sum",
                "granularity": "day",
            },
        )
    )

    assert "FROM user_orders" in sql
    assert "SUM(METRIC_VALUE_SOURCE)" in sql.upper()
    assert "ANALYSIS_TYPE: TREND" in sql.upper()
