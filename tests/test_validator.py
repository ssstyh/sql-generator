import pytest

from core import InputValidator, ValidationError


def test_validator_rejects_invalid_identifier() -> None:
    validator = InputValidator()

    with pytest.raises(ValidationError):
        validator.validate_request(
            analysis_type="trend",
            dialect="mysql",
            parameters={
                "table_name": "user-orders",
                "date_field": "order_date",
                "metric_field": "amount",
            },
        )


def test_validator_requires_steps_for_funnel() -> None:
    validator = InputValidator()

    with pytest.raises(ValidationError):
        validator.validate_request(
            analysis_type="funnel",
            dialect="mysql",
            parameters={
                "table_name": "events",
                "user_id_field": "user_id",
                "date_field": "event_time",
                "steps": [],
            },
        )


def test_validator_rejects_invalid_funnel_step_shape() -> None:
    validator = InputValidator()

    with pytest.raises(ValidationError):
        validator.validate_request(
            analysis_type="funnel",
            dialect="mysql",
            parameters={
                "table_name": "events",
                "user_id_field": "user_id",
                "date_field": "event_time",
                "steps": ["view", "purchase"],
            },
        )


def test_validator_adds_default_aggregation() -> None:
    validator = InputValidator()
    parameters = validator.validate_request(
        analysis_type="compare",
        dialect="postgresql",
        parameters={
            "table_name": "user_orders",
            "date_field": "order_date",
            "metric_field": "amount",
            "granularity": "month",
            "comparison_type": "mom",
        },
    )

    assert parameters["aggregation"] == "sum"


def test_validator_rejects_invalid_granularity() -> None:
    validator = InputValidator()

    with pytest.raises(ValidationError):
        validator.validate_request(
            analysis_type="trend",
            dialect="mysql",
            parameters={
                "table_name": "user_orders",
                "date_field": "order_date",
                "metric_field": "amount",
                "granularity": "quarter",
            },
        )


def test_validator_rejects_invalid_comparison_type() -> None:
    validator = InputValidator()

    with pytest.raises(ValidationError):
        validator.validate_request(
            analysis_type="compare",
            dialect="mysql",
            parameters={
                "table_name": "user_orders",
                "date_field": "order_date",
                "metric_field": "amount",
                "granularity": "week",
                "comparison_type": "wow",
            },
        )


def test_validator_rejects_invalid_retention_mode() -> None:
    validator = InputValidator()

    with pytest.raises(ValidationError):
        validator.validate_request(
            analysis_type="retention",
            dialect="postgresql",
            parameters={
                "table_name": "user_events",
                "user_id_field": "user_id",
                "date_field": "event_time",
                "retention_days": [1, 7],
                "retention_mode": "matrix",
            },
        )


def test_validator_normalizes_retention_days() -> None:
    validator = InputValidator()
    parameters = validator.validate_request(
        analysis_type="retention",
        dialect="postgresql",
        parameters={
            "table_name": "user_events",
            "user_id_field": "user_id",
            "date_field": "event_time",
            "retention_days": [7, 1, 7, 3],
            "retention_mode": "curve",
        },
    )

    assert parameters["retention_days"] == [1, 3, 7]


def test_validator_rejects_invalid_date_range() -> None:
    validator = InputValidator()

    with pytest.raises(ValidationError):
        validator.validate_request(
            analysis_type="trend",
            dialect="mysql",
            parameters={
                "table_name": "user_orders",
                "date_field": "order_date",
                "metric_field": "amount",
                "granularity": "day",
                "date_range": {"start": "2026-01-08", "end": "2026-01-01"},
            },
        )


def test_validator_rejects_invalid_filter_conditions() -> None:
    validator = InputValidator()

    with pytest.raises(ValidationError):
        validator.validate_request(
            analysis_type="compare",
            dialect="mysql",
            parameters={
                "table_name": "user_orders",
                "date_field": "order_date",
                "metric_field": "amount",
                "granularity": "week",
                "comparison_type": "mom",
                "filter_conditions": [
                    {"field": "channel", "operator": "IN", "value": []},
                ],
            },
        )


def test_validator_adds_default_rfm_analysis_date_and_bins() -> None:
    validator = InputValidator()
    parameters = validator.validate_request(
        analysis_type="rfm",
        dialect="postgresql",
        parameters={
            "table_name": "user_orders",
            "user_id_field": "user_id",
            "date_field": "order_date",
            "amount_field": "amount",
        },
    )

    assert parameters["analysis_date"]
    assert parameters["r_bins"] == 5
    assert parameters["f_bins"] == 5
    assert parameters["m_bins"] == 5


def test_validator_rejects_invalid_rfm_bin_value() -> None:
    validator = InputValidator()

    with pytest.raises(ValidationError):
        validator.validate_request(
            analysis_type="rfm",
            dialect="mysql",
            parameters={
                "table_name": "user_orders",
                "user_id_field": "user_id",
                "date_field": "order_date",
                "amount_field": "amount",
                "r_bins": 1,
            },
        )
