from core import GenerationRequest, SQLGenerator


def test_rfm_sql_supports_mysql_scoring_and_segments() -> None:
    generator = SQLGenerator()

    sql = generator.generate(
        GenerationRequest(
            analysis_type="rfm",
            dialect="mysql",
            parameters={
                "table_name": "user_orders",
                "user_id_field": "user_id",
                "date_field": "order_date",
                "amount_field": "amount",
                "analysis_date": "2026-03-31",
            },
        )
    )

    sql_upper = sql.upper()
    assert "DATEDIFF('2026-03-31', MAX(ORDER_DATE)) AS RECENCY_DAYS" in sql_upper
    assert "COUNT(*) AS FREQUENCY_VALUE" in sql_upper
    assert "NTILE(5) OVER" in sql_upper
    assert "ORDER BY FREQUENCY_VALUE ASC, USER_ID ASC" in sql_upper
    assert "AS F_SCORE" in sql_upper
    assert "CONCAT(R_SCORE, F_SCORE, M_SCORE) AS RFM_SCORE" in sql_upper
    assert "SEGMENT_LABEL" in sql_upper


def test_rfm_sql_supports_postgresql_bins_and_filters() -> None:
    generator = SQLGenerator()

    sql = generator.generate(
        GenerationRequest(
            analysis_type="rfm",
            dialect="postgresql",
            parameters={
                "table_name": "user_orders",
                "user_id_field": "user_id",
                "date_field": "order_date",
                "amount_field": "amount",
                "analysis_date": "2026-03-31",
                "r_bins": 4,
                "f_bins": 4,
                "m_bins": 3,
                "filter_conditions": [
                    {"field": "region", "operator": "=", "value": "APAC"},
                ],
            },
        )
    )

    sql_upper = sql.upper()
    assert "('2026-03-31'::DATE - MAX(ORDER_DATE)) AS RECENCY_DAYS" in sql_upper
    assert "NTILE(4) OVER" in sql_upper
    assert "ORDER BY RECENCY_DAYS ASC, USER_ID ASC" in sql_upper
    assert "NTILE(3) OVER" in sql_upper
    assert "ORDER BY MONETARY_VALUE ASC, USER_ID ASC" in sql_upper
    assert "REGION = 'APAC'" in sql_upper
    assert "CHAMPIONS" in sql_upper
