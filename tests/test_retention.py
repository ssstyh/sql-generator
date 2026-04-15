from core import GenerationRequest, SQLGenerator


def test_retention_table_sql_supports_mysql_days_and_columns() -> None:
    generator = SQLGenerator()

    sql = generator.generate(
        GenerationRequest(
            analysis_type="retention",
            dialect="mysql",
            parameters={
                "table_name": "user_events",
                "user_id_field": "user_id",
                "date_field": "event_time",
                "retention_days": [1, 3, 7, 14, 30],
                "retention_mode": "table",
                "start_date": "2026-01-01",
                "end_date": "2026-01-31",
            },
        )
    )

    sql_upper = sql.upper()
    assert "DAY_30_USERS" in sql_upper
    assert "DAY_30_RATE" in sql_upper
    assert "DATE_ADD(FA.COHORT_DATE, INTERVAL 30 DAY)" in sql_upper
    assert "COHORT_SIZE" in sql_upper


def test_retention_curve_sql_supports_postgresql_interval_and_filters() -> None:
    generator = SQLGenerator()

    sql = generator.generate(
        GenerationRequest(
            analysis_type="retention",
            dialect="postgresql",
            parameters={
                "table_name": "user_events",
                "user_id_field": "user_id",
                "date_field": "event_time",
                "retention_days": [7, 1, 3, 7],
                "retention_mode": "curve",
                "filter_conditions": [
                    {"field": "event_type", "operator": "IN", "value": ["login", "purchase"]},
                ],
            },
        )
    )

    sql_upper = sql.upper()
    assert "RETENTION_DAY" in sql_upper
    assert "RETAINED_USERS" in sql_upper
    assert "RETENTION_RATE" in sql_upper
    assert "INTERVAL '7 DAY'" in sql_upper
    assert "EVENT_TYPE IN" in sql_upper
    assert "'LOGIN'" in sql_upper
    assert "'PURCHASE'" in sql_upper


def test_retention_curve_sql_orders_normalized_days() -> None:
    generator = SQLGenerator()

    sql = generator.generate(
        GenerationRequest(
            analysis_type="retention",
            dialect="postgresql",
            parameters={
                "table_name": "user_events",
                "user_id_field": "user_id",
                "date_field": "event_time",
                "retention_days": [14, 1, 7],
                "retention_mode": "curve",
            },
        )
    )

    day_1_index = sql.index("1 AS retention_day")
    day_7_index = sql.index("7 AS retention_day")
    day_14_index = sql.index("14 AS retention_day")
    assert day_1_index < day_7_index < day_14_index
