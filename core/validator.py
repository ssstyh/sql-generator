from __future__ import annotations

from datetime import datetime
import re
from typing import Any


SUPPORTED_DIALECTS = {"mysql", "postgresql"}
SUPPORTED_AGGREGATIONS = {"sum", "count", "avg", "min", "max", "count_distinct"}
SUPPORTED_GRANULARITIES = {"day", "week", "month"}
SUPPORTED_COMPARISON_TYPES = {"yoy", "mom"}
SUPPORTED_RETENTION_MODES = {"table", "curve"}
SUPPORTED_FILTER_OPERATORS = {"=", "!=", ">", ">=", "<", "<=", "IN", "LIKE"}
IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

REQUIRED_FIELDS: dict[str, tuple[str, ...]] = {
    "trend": ("table_name", "date_field", "metric_field", "granularity"),
    "compare": (
        "table_name",
        "date_field",
        "metric_field",
        "granularity",
        "comparison_type",
    ),
    "retention": (
        "table_name",
        "user_id_field",
        "date_field",
        "retention_days",
        "retention_mode",
    ),
    "funnel": ("table_name", "user_id_field", "date_field", "steps"),
    "rfm": ("table_name", "user_id_field", "date_field", "amount_field"),
}

IDENTIFIER_FIELDS = {
    "table_name",
    "user_id_field",
    "date_field",
    "metric_field",
    "amount_field",
}


class ValidationError(ValueError):
    """Raised when user input cannot safely enter the generator pipeline."""


class InputValidator:
    """Validate request shape, analysis parameters, and shared identifier rules."""

    def validate_request(
        self,
        *,
        analysis_type: str,
        parameters: dict[str, Any],
        dialect: str,
    ) -> dict[str, Any]:
        if analysis_type not in REQUIRED_FIELDS:
            raise ValidationError(f"Unsupported analysis type: {analysis_type}")

        if dialect not in SUPPORTED_DIALECTS:
            raise ValidationError(f"Unsupported SQL dialect: {dialect}")

        normalized: dict[str, Any] = dict(parameters)
        self._validate_required_fields(analysis_type, normalized)
        self._validate_identifiers(normalized)
        self._validate_aggregation(normalized)
        self._validate_granularity(normalized)
        self._validate_comparison_type(normalized)
        self._validate_retention_mode(normalized)
        self._validate_retention_days(normalized)
        self._validate_date_range(normalized)
        self._validate_start_end_dates(normalized)
        self._validate_filter_conditions(normalized)
        self._validate_steps(normalized)
        return normalized

    def _validate_required_fields(
        self,
        analysis_type: str,
        parameters: dict[str, Any],
    ) -> None:
        required_fields = REQUIRED_FIELDS[analysis_type]
        missing = [
            field
            for field in required_fields
            if field not in parameters or self._is_empty_value(parameters[field])
        ]
        if missing:
            joined = ", ".join(missing)
            raise ValidationError(f"Missing required parameters for {analysis_type}: {joined}")

    def _validate_identifiers(self, parameters: dict[str, Any]) -> None:
        for field_name in IDENTIFIER_FIELDS:
            if field_name not in parameters:
                continue
            parameters[field_name] = self._normalize_identifier(field_name, parameters[field_name])

    def _validate_aggregation(self, parameters: dict[str, Any]) -> None:
        aggregation = parameters.get("aggregation")
        if aggregation is None:
            parameters["aggregation"] = "sum"
            return

        if not isinstance(aggregation, str) or not aggregation.strip():
            raise ValidationError("Parameter 'aggregation' must be a non-empty string.")

        normalized_aggregation = aggregation.strip().lower()
        if normalized_aggregation not in SUPPORTED_AGGREGATIONS:
            joined = ", ".join(sorted(SUPPORTED_AGGREGATIONS))
            raise ValidationError(f"Unsupported aggregation: {aggregation}. Allowed: {joined}")
        parameters["aggregation"] = normalized_aggregation

    def _validate_granularity(self, parameters: dict[str, Any]) -> None:
        granularity = parameters.get("granularity")
        if granularity is None:
            return

        if not isinstance(granularity, str) or not granularity.strip():
            raise ValidationError("Parameter 'granularity' must be a non-empty string.")

        normalized_granularity = granularity.strip().lower()
        if normalized_granularity not in SUPPORTED_GRANULARITIES:
            joined = ", ".join(sorted(SUPPORTED_GRANULARITIES))
            raise ValidationError(f"Unsupported granularity: {granularity}. Allowed: {joined}")
        parameters["granularity"] = normalized_granularity

    def _validate_comparison_type(self, parameters: dict[str, Any]) -> None:
        comparison_type = parameters.get("comparison_type")
        if comparison_type is None:
            return

        if not isinstance(comparison_type, str) or not comparison_type.strip():
            raise ValidationError("Parameter 'comparison_type' must be a non-empty string.")

        normalized_comparison_type = comparison_type.strip().lower()
        if normalized_comparison_type not in SUPPORTED_COMPARISON_TYPES:
            joined = ", ".join(sorted(SUPPORTED_COMPARISON_TYPES))
            raise ValidationError(
                f"Unsupported comparison_type: {comparison_type}. Allowed: {joined}"
            )
        parameters["comparison_type"] = normalized_comparison_type

    def _validate_retention_mode(self, parameters: dict[str, Any]) -> None:
        retention_mode = parameters.get("retention_mode")
        if retention_mode is None:
            return

        if not isinstance(retention_mode, str) or not retention_mode.strip():
            raise ValidationError("Parameter 'retention_mode' must be a non-empty string.")

        normalized_retention_mode = retention_mode.strip().lower()
        if normalized_retention_mode not in SUPPORTED_RETENTION_MODES:
            joined = ", ".join(sorted(SUPPORTED_RETENTION_MODES))
            raise ValidationError(f"Unsupported retention_mode: {retention_mode}. Allowed: {joined}")
        parameters["retention_mode"] = normalized_retention_mode

    def _validate_retention_days(self, parameters: dict[str, Any]) -> None:
        retention_days = parameters.get("retention_days")
        if retention_days is None:
            return
        if not isinstance(retention_days, list) or not retention_days:
            raise ValidationError("Parameter 'retention_days' must be a non-empty list.")

        normalized_days: list[int] = []
        for day in retention_days:
            if isinstance(day, bool) or not isinstance(day, int) or day <= 0:
                raise ValidationError("Each retention day must be a positive integer.")
            normalized_days.append(day)
        parameters["retention_days"] = sorted(set(normalized_days))

    def _validate_date_range(self, parameters: dict[str, Any]) -> None:
        date_range = parameters.get("date_range")
        if date_range is None:
            return
        if not isinstance(date_range, dict):
            raise ValidationError("Parameter 'date_range' must be an object with start and end.")

        start = date_range.get("start")
        end = date_range.get("end")
        if self._is_empty_value(start) or self._is_empty_value(end):
            raise ValidationError("Parameter 'date_range' requires non-empty start and end.")

        start_date = self._parse_iso_date("date_range.start", start)
        end_date = self._parse_iso_date("date_range.end", end)
        if start_date > end_date:
            raise ValidationError("Parameter 'date_range' start cannot be after end.")

        parameters["date_range"] = {
            "start": start.strip(),
            "end": end.strip(),
        }

    def _validate_start_end_dates(self, parameters: dict[str, Any]) -> None:
        start_date = parameters.get("start_date")
        end_date = parameters.get("end_date")

        normalized_start: str | None = None
        normalized_end: str | None = None
        start_date_value = None
        end_date_value = None

        if start_date is not None:
            if self._is_empty_value(start_date):
                raise ValidationError("Parameter 'start_date' cannot be blank.")
            start_date_value = self._parse_iso_date("start_date", start_date)
            normalized_start = start_date.strip()

        if end_date is not None:
            if self._is_empty_value(end_date):
                raise ValidationError("Parameter 'end_date' cannot be blank.")
            end_date_value = self._parse_iso_date("end_date", end_date)
            normalized_end = end_date.strip()

        if start_date_value and end_date_value and start_date_value > end_date_value:
            raise ValidationError("Parameter 'start_date' cannot be after 'end_date'.")

        if normalized_start is not None:
            parameters["start_date"] = normalized_start
        if normalized_end is not None:
            parameters["end_date"] = normalized_end

    def _validate_filter_conditions(self, parameters: dict[str, Any]) -> None:
        filter_conditions = parameters.get("filter_conditions")
        if filter_conditions is None:
            parameters["filter_conditions"] = []
            return
        if not isinstance(filter_conditions, list):
            raise ValidationError("Parameter 'filter_conditions' must be a list of condition objects.")

        normalized_conditions: list[dict[str, Any]] = []
        for index, condition in enumerate(filter_conditions, start=1):
            if not isinstance(condition, dict) or not condition:
                raise ValidationError(
                    f"Filter condition #{index} must be an object with field, operator, and value."
                )

            field = condition.get("field")
            operator = condition.get("operator")
            if self._is_empty_value(field) or self._is_empty_value(operator) or "value" not in condition:
                raise ValidationError(
                    f"Filter condition #{index} requires field, operator, and value."
                )

            normalized_conditions.append(
                {
                    "field": self._normalize_identifier("filter_conditions.field", field),
                    "operator": self._normalize_operator(operator),
                    "value": self._normalize_filter_value(
                        index,
                        self._normalize_operator(operator),
                        condition["value"],
                    ),
                }
            )

        parameters["filter_conditions"] = normalized_conditions

    def _validate_steps(self, parameters: dict[str, Any]) -> None:
        steps = parameters.get("steps")
        if steps is None:
            return
        if not isinstance(steps, list) or not steps:
            raise ValidationError("Parameter 'steps' must be a non-empty list.")

        normalized_steps: list[str] = []
        for step in steps:
            if not isinstance(step, str) or not step.strip():
                raise ValidationError("Each funnel step must be a non-empty string.")
            normalized_steps.append(step.strip())
        parameters["steps"] = normalized_steps

    def _normalize_operator(self, operator: Any) -> str:
        if not isinstance(operator, str) or not operator.strip():
            raise ValidationError("Filter operator must be a non-empty string.")

        normalized_operator = operator.strip().upper()
        if normalized_operator not in SUPPORTED_FILTER_OPERATORS:
            joined = ", ".join(sorted(SUPPORTED_FILTER_OPERATORS))
            raise ValidationError(f"Unsupported filter operator: {operator}. Allowed: {joined}")
        return normalized_operator

    def _normalize_filter_value(self, index: int, operator: str, value: Any) -> Any:
        if operator == "IN":
            if not isinstance(value, list) or not value:
                raise ValidationError(
                    f"Filter condition #{index} with operator IN requires a non-empty list value."
                )
            return [self._normalize_scalar_value(index, item) for item in value]

        if operator == "LIKE":
            normalized_like_value = self._normalize_scalar_value(index, value)
            if not isinstance(normalized_like_value, str):
                raise ValidationError(
                    f"Filter condition #{index} with operator LIKE requires a string value."
                )
            return normalized_like_value

        if isinstance(value, list):
            raise ValidationError(
                f"Filter condition #{index} only supports list values when operator is IN."
            )
        return self._normalize_scalar_value(index, value)

    def _normalize_scalar_value(self, index: int, value: Any) -> Any:
        if isinstance(value, str):
            if not value.strip():
                raise ValidationError(f"Filter condition #{index} value cannot be blank.")
            return value.strip()
        if isinstance(value, (int, float, bool)) or value is None:
            return value
        raise ValidationError(
            f"Filter condition #{index} value must be a scalar or list of scalars."
        )

    def _normalize_identifier(self, field_name: str, value: Any) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValidationError(f"Invalid identifier for {field_name}: {value!r}.")
        normalized_value = value.strip()
        if not IDENTIFIER_PATTERN.fullmatch(normalized_value):
            raise ValidationError(
                f"Invalid identifier for {field_name}: {value!r}. "
                "Only letters, numbers, and underscores are allowed."
            )
        return normalized_value

    def _parse_iso_date(self, field_name: str, value: Any) -> datetime.date:
        if not isinstance(value, str):
            raise ValidationError(f"Parameter '{field_name}' must use YYYY-MM-DD format.")
        try:
            return datetime.strptime(value.strip(), "%Y-%m-%d").date()
        except ValueError as exc:
            raise ValidationError(f"Parameter '{field_name}' must use YYYY-MM-DD format.") from exc

    def _is_empty_value(self, value: Any) -> bool:
        if value is None:
            return True
        if isinstance(value, str):
            return not value.strip()
        return False
