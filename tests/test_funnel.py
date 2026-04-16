from core import GenerationRequest, SQLGenerator


def test_funnel_sql_supports_ordered_mysql_steps() -> None:
    generator = SQLGenerator()

    sql = generator.generate(
        GenerationRequest(
            analysis_type="funnel",
            dialect="mysql",
            parameters={
                "table_name": "user_events",
                "user_id_field": "user_id",
                "date_field": "event_time",
                "window_days": 7,
                "date_range": {"start": "2026-03-01", "end": "2026-03-31"},
                "steps": [
                    {
                        "step_name": "view_product",
                        "filter_conditions": [
                            {"field": "event_name", "operator": "=", "value": "view_product"},
                        ],
                    },
                    {
                        "step_name": "add_to_cart",
                        "filter_conditions": [
                            {"field": "event_name", "operator": "=", "value": "add_to_cart"},
                        ],
                    },
                    {
                        "step_name": "purchase",
                        "filter_conditions": [
                            {"field": "event_name", "operator": "=", "value": "purchase"},
                        ],
                    },
                ],
            },
        )
    )

    sql_upper = sql.upper()
    assert "STEP_ORDER" in sql_upper
    assert "CONVERSION_RATE" in sql_upper
    assert "OVERALL_CONVERSION_RATE" in sql_upper
    assert "DATE_ADD(PREV.STEP_TIME, INTERVAL 7 DAY)" in sql_upper
    assert "'VIEW_PRODUCT' AS STEP_NAME" in sql_upper
    assert "EVENT_NAME = 'PURCHASE'" in sql_upper


def test_funnel_sql_supports_postgresql_window_and_common_filters() -> None:
    generator = SQLGenerator()

    sql = generator.generate(
        GenerationRequest(
            analysis_type="funnel",
            dialect="postgresql",
            parameters={
                "table_name": "user_events",
                "user_id_field": "user_id",
                "date_field": "event_time",
                "window_days": 14,
                "filter_conditions": [
                    {"field": "platform", "operator": "IN", "value": ["ios", "android"]},
                ],
                "steps": [
                    {
                        "step_name": "signup",
                        "filter_conditions": [
                            {"field": "event_name", "operator": "=", "value": "signup"},
                        ],
                    },
                    {
                        "step_name": "activate",
                        "filter_conditions": [
                            {"field": "event_name", "operator": "=", "value": "activate"},
                        ],
                    },
                ],
            },
        )
    )

    sql_upper = sql.upper()
    assert "INTERVAL '14 DAY'" in sql_upper
    assert "FIRST_VALUE(USER_COUNT) OVER" in sql_upper
    assert "PLATFORM IN" in sql_upper
    assert "'IOS'" in sql_upper
    assert "'ANDROID'" in sql_upper
    assert "INNER JOIN STEP_1_USERS PREV" in sql_upper
