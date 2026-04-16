from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from core.validator import InputValidator
from utils.formatter import SQLFormatter


ANALYSIS_TEMPLATES = {
    "trend": "trend.sql.j2",
    "compare": "compare.sql.j2",
    "retention": "retention.sql.j2",
    "funnel": "funnel.sql.j2",
    "rfm": "rfm.sql.j2",
}


@dataclass(slots=True)
class GenerationRequest:
    """Normalized input passed to the SQL generation pipeline."""

    analysis_type: str
    parameters: dict[str, Any] = field(default_factory=dict)
    dialect: str = "mysql"


class SQLGenerator:
    """Render SQL templates through a single validation and formatting facade."""

    def __init__(
        self,
        template_dir: Path | None = None,
        validator: InputValidator | None = None,
        formatter: SQLFormatter | None = None,
    ) -> None:
        base_dir = Path(__file__).resolve().parent.parent
        self.template_dir = template_dir or (base_dir / "templates")
        self.validator = validator or InputValidator()
        self.formatter = formatter or SQLFormatter()
        self.environment = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
            undefined=StrictUndefined,
        )

    def list_supported_analyses(self) -> list[str]:
        return sorted(ANALYSIS_TEMPLATES)

    def generate(
        self,
        request: GenerationRequest | None = None,
        *,
        analysis_type: str | None = None,
        parameters: dict[str, Any] | None = None,
        dialect: str = "mysql",
    ) -> str:
        normalized_request = request or GenerationRequest(
            analysis_type=analysis_type or "",
            parameters=parameters or {},
            dialect=dialect,
        )
        validated_parameters = self.validator.validate_request(
            analysis_type=normalized_request.analysis_type,
            parameters=normalized_request.parameters,
            dialect=normalized_request.dialect,
        )
        template_context = self._build_template_context(
            analysis_type=normalized_request.analysis_type,
            parameters=validated_parameters,
            dialect=normalized_request.dialect,
        )

        template_name = ANALYSIS_TEMPLATES[normalized_request.analysis_type]
        template = self.environment.get_template(template_name)
        rendered_sql = template.render(
            analysis_type=normalized_request.analysis_type,
            dialect=normalized_request.dialect,
            generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"),
            **template_context,
        )
        return self.formatter.format_sql(rendered_sql)

    def _build_template_context(
        self,
        *,
        analysis_type: str,
        parameters: dict[str, Any],
        dialect: str,
    ) -> dict[str, Any]:
        context_builders = {
            "trend": self._build_trend_context,
            "compare": self._build_compare_context,
            "retention": self._build_retention_context,
            "funnel": self._build_funnel_context,
            "rfm": self._build_rfm_context,
        }

        builder = context_builders.get(analysis_type)
        if builder is None:
            return dict(parameters)
        return builder(parameters, dialect)

    def _build_trend_context(self, parameters: dict[str, Any], dialect: str) -> dict[str, Any]:
        context = dict(parameters)
        context.update(
            {
                "analysis_label": "趋势分析",
                "comment_lines": self._build_comment_lines(
                    analysis_type="trend",
                    parameters=parameters,
                ),
                "period_expression": self._build_period_expression(
                    parameters["date_field"],
                    dialect,
                    parameters["granularity"],
                ),
                "metric_expression": self._build_metric_expression(
                    parameters["aggregation"],
                    "metric_value_source",
                ),
                "where_clause": self._build_where_clause(
                    date_field=parameters["date_field"],
                    dialect=dialect,
                    filter_conditions=parameters.get("filter_conditions", []),
                    date_range=parameters.get("date_range"),
                ),
            }
        )
        return context

    def _build_compare_context(self, parameters: dict[str, Any], dialect: str) -> dict[str, Any]:
        context = self._build_trend_context(parameters, dialect)
        context.update(
            {
                "analysis_label": "同比/环比分析",
                "comment_lines": self._build_comment_lines(
                    analysis_type="compare",
                    parameters=parameters,
                ),
                "yoy_previous_period_expression": self._add_years_expression(
                    "prev.period_start",
                    1,
                    dialect,
                ),
            }
        )
        return context

    def _build_retention_context(self, parameters: dict[str, Any], dialect: str) -> dict[str, Any]:
        context = dict(parameters)
        max_retention_day = max(parameters["retention_days"])
        context.update(
            {
                "analysis_label": "留存分析",
                "comment_lines": self._build_comment_lines(
                    analysis_type="retention",
                    parameters=parameters,
                ),
                "activity_date_expression": self._build_activity_date_expression(
                    parameters["date_field"],
                    dialect,
                ),
                "where_clause": self._build_where_clause(
                    date_field=parameters["date_field"],
                    dialect=dialect,
                    filter_conditions=parameters.get("filter_conditions", []),
                    start_date=parameters.get("start_date"),
                    end_date=parameters.get("end_date"),
                ),
                "retention_day_expressions": {
                    day: self._add_days_expression(
                        "fa.cohort_date",
                        day,
                        dialect,
                        cast_to_date=True,
                    )
                    for day in parameters["retention_days"]
                },
                "max_retention_date_expression": self._add_days_expression(
                    "fa.cohort_date",
                    max_retention_day,
                    dialect,
                    cast_to_date=True,
                ),
            }
        )
        return context

    def _build_funnel_context(self, parameters: dict[str, Any], dialect: str) -> dict[str, Any]:
        context = dict(parameters)
        funnel_steps: list[dict[str, Any]] = []
        common_filters = parameters.get("filter_conditions", [])

        for index, step in enumerate(parameters["steps"], start=1):
            step_table = step.get("table_name", parameters["table_name"])
            step_user_id = step.get("user_id_field", parameters["user_id_field"])
            step_date_field = step.get("date_field", parameters["date_field"])
            previous_result_cte = None if index == 1 else f"step_{index - 1}_users"
            funnel_steps.append(
                {
                    "step_order": index,
                    "step_name": step["step_name"],
                    "step_name_literal": self._render_literal(step["step_name"]),
                    "source_cte_name": f"step_{index}_source",
                    "result_cte_name": f"step_{index}_users",
                    "table_name": step_table,
                    "user_id_field": step_user_id,
                    "date_field": step_date_field,
                    "where_clause": self._build_where_clause(
                        date_field=step_date_field,
                        dialect=dialect,
                        filter_conditions=[*common_filters, *step.get("filter_conditions", [])],
                        date_range=parameters.get("date_range"),
                    ),
                    "previous_result_cte_name": previous_result_cte,
                    "window_end_expression": (
                        self._add_days_expression("prev.step_time", parameters["window_days"], dialect)
                        if previous_result_cte
                        else None
                    ),
                }
            )

        context.update(
            {
                "analysis_label": "Funnel Analysis",
                "comment_lines": self._build_comment_lines(
                    analysis_type="funnel",
                    parameters=parameters,
                ),
                "funnel_steps": funnel_steps,
            }
        )
        return context

    def _build_rfm_context(self, parameters: dict[str, Any], dialect: str) -> dict[str, Any]:
        context = dict(parameters)
        analysis_date_literal = self._render_literal(parameters["analysis_date"])
        r_high_threshold = max(2, parameters["r_bins"] - 1)
        f_high_threshold = max(2, parameters["f_bins"] - 1)
        m_high_threshold = max(2, parameters["m_bins"] - 1)
        context.update(
            {
                "analysis_label": "RFM Analysis",
                "comment_lines": self._build_comment_lines(
                    analysis_type="rfm",
                    parameters=parameters,
                ),
                "activity_date_expression": self._build_activity_date_expression(
                    parameters["date_field"],
                    dialect,
                ),
                "analysis_date_literal": analysis_date_literal,
                "where_clause": self._build_where_clause(
                    date_field=parameters["date_field"],
                    dialect=dialect,
                    filter_conditions=parameters.get("filter_conditions", []),
                    end_date=parameters["analysis_date"],
                ),
                "recency_expression": self._build_recency_expression(
                    analysis_date_literal,
                    dialect,
                ),
                "r_score_expression": (
                    f"{parameters['r_bins']} + 1 - NTILE({parameters['r_bins']}) "
                    "OVER (ORDER BY recency_days ASC, user_id ASC)"
                ),
                "f_score_expression": (
                    f"NTILE({parameters['f_bins']}) OVER (ORDER BY frequency_value ASC, user_id ASC)"
                ),
                "m_score_expression": (
                    f"NTILE({parameters['m_bins']}) OVER (ORDER BY monetary_value ASC, user_id ASC)"
                ),
                "rfm_score_expression": "CONCAT(r_score, f_score, m_score)",
                "segment_case_sql": self._build_rfm_segment_case_sql(
                    r_high_threshold=r_high_threshold,
                    f_high_threshold=f_high_threshold,
                    m_high_threshold=m_high_threshold,
                ),
            }
        )
        return context

    def _build_comment_lines(
        self,
        *,
        analysis_type: str,
        parameters: dict[str, Any],
    ) -> list[str]:
        if analysis_type == "funnel":
            lines = [
                f"description: ordered funnel with {len(parameters['steps'])} steps",
                f"window_days: {parameters['window_days']}",
                "step_names: " + ", ".join(step["step_name"] for step in parameters["steps"]),
            ]
            if parameters.get("date_range"):
                lines.append(
                    "date_range: "
                    f"{parameters['date_range']['start']} ~ {parameters['date_range']['end']}"
                )
        elif analysis_type == "rfm":
            lines = [
                "description: user-level recency, frequency, and monetary scoring",
                f"analysis_date: {parameters['analysis_date']}",
                (
                    "bins: "
                    f"r={parameters['r_bins']}, f={parameters['f_bins']}, m={parameters['m_bins']}"
                ),
            ]
        elif analysis_type == "trend":
            lines = [
                f"说明: 输出 {parameters['granularity']} 粒度趋势指标",
                f"聚合方式: {parameters['aggregation']}",
            ]
            if parameters.get("date_range"):
                lines.append(
                    "日期范围: "
                    f"{parameters['date_range']['start']} ~ {parameters['date_range']['end']}"
                )
        elif analysis_type == "compare":
            comparison_label = "同比" if parameters["comparison_type"] == "yoy" else "环比"
            lines = [
                f"说明: 输出 {comparison_label}对比结果",
                f"时间粒度: {parameters['granularity']}",
                f"聚合方式: {parameters['aggregation']}",
            ]
            if parameters.get("date_range"):
                lines.append(
                    "日期范围: "
                    f"{parameters['date_range']['start']} ~ {parameters['date_range']['end']}"
                )
        else:
            lines = [
                "说明: cohort 当天首次活跃，N 天后当天再次活跃即记为留存",
                f"输出模式: {parameters['retention_mode']}",
                f"留存天数: {', '.join(str(day) for day in parameters['retention_days'])}",
            ]
            if parameters.get("start_date") or parameters.get("end_date"):
                lines.append(
                    "活跃过滤范围: "
                    f"{parameters.get('start_date', '未限制')} ~ {parameters.get('end_date', '未限制')}"
                )

        lines.append(f"筛选条件数: {len(parameters.get('filter_conditions', []))}")
        return lines

    def _build_period_expression(self, date_field: str, dialect: str, granularity: str) -> str:
        if dialect == "mysql":
            if granularity == "day":
                return f"DATE({date_field})"
            if granularity == "week":
                return f"DATE_SUB(DATE({date_field}), INTERVAL WEEKDAY({date_field}) DAY)"
            return f"DATE_SUB(DATE({date_field}), INTERVAL DAYOFMONTH({date_field}) - 1 DAY)"

        return f"DATE_TRUNC('{granularity}', {date_field})::date"

    def _build_activity_date_expression(self, date_field: str, dialect: str) -> str:
        if dialect == "mysql":
            return f"DATE({date_field})"
        return f"({date_field})::date"

    def _build_metric_expression(self, aggregation: str, metric_field: str) -> str:
        if aggregation == "count":
            return "COUNT(*)"
        if aggregation == "count_distinct":
            return f"COUNT(DISTINCT {metric_field})"
        return f"{aggregation.upper()}({metric_field})"

    def _build_recency_expression(self, analysis_date_literal: str, dialect: str) -> str:
        if dialect == "mysql":
            return f"DATEDIFF({analysis_date_literal}, MAX(order_date))"
        return f"({analysis_date_literal}::date - MAX(order_date))"

    def _build_rfm_segment_case_sql(
        self,
        *,
        r_high_threshold: int,
        f_high_threshold: int,
        m_high_threshold: int,
    ) -> str:
        return "\n".join(
            [
                "CASE",
                (
                    f"  WHEN r_score >= {r_high_threshold} AND f_score >= {f_high_threshold} "
                    f"AND m_score >= {m_high_threshold} THEN 'champions'"
                ),
                (
                    f"  WHEN r_score >= {r_high_threshold} AND f_score >= {f_high_threshold} "
                    f"AND m_score < {m_high_threshold} THEN 'loyal_customers'"
                ),
                (
                    f"  WHEN r_score >= {r_high_threshold} AND f_score < {f_high_threshold} "
                    f"AND m_score >= {m_high_threshold} THEN 'big_spenders'"
                ),
                (
                    f"  WHEN r_score >= {r_high_threshold} AND f_score < {f_high_threshold} "
                    f"AND m_score < {m_high_threshold} THEN 'potential_loyalists'"
                ),
                (
                    f"  WHEN r_score < {r_high_threshold} AND f_score >= {f_high_threshold} "
                    f"AND m_score >= {m_high_threshold} THEN 'at_risk_vips'"
                ),
                (
                    f"  WHEN r_score < {r_high_threshold} AND f_score >= {f_high_threshold} "
                    f"AND m_score < {m_high_threshold} THEN 'needs_attention'"
                ),
                (
                    f"  WHEN r_score < {r_high_threshold} AND f_score < {f_high_threshold} "
                    f"AND m_score >= {m_high_threshold} THEN 'one_time_big_spenders'"
                ),
                "  ELSE 'hibernating'",
                "END",
            ]
        )

    def _build_where_clause(
        self,
        *,
        date_field: str,
        dialect: str,
        filter_conditions: list[dict[str, Any]],
        date_range: dict[str, str] | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> str:
        clauses: list[str] = []
        activity_date_expression = self._build_activity_date_expression(date_field, dialect)

        if date_range is not None:
            clauses.append(
                f"{activity_date_expression} >= {self._render_literal(date_range['start'])}"
            )
            clauses.append(
                f"{activity_date_expression} <= {self._render_literal(date_range['end'])}"
            )

        if start_date is not None:
            clauses.append(f"{activity_date_expression} >= {self._render_literal(start_date)}")

        if end_date is not None:
            clauses.append(f"{activity_date_expression} <= {self._render_literal(end_date)}")

        for condition in filter_conditions:
            field = condition["field"]
            operator = condition["operator"]
            value = condition["value"]

            if operator == "IN":
                rendered_values = ", ".join(self._render_literal(item) for item in value)
                clauses.append(f"{field} IN ({rendered_values})")
            else:
                clauses.append(f"{field} {operator} {self._render_literal(value)}")

        if not clauses:
            return "1 = 1"

        return "1 = 1\n    AND " + "\n    AND ".join(clauses)

    def _render_literal(self, value: Any) -> str:
        if value is None:
            return "NULL"
        if isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str):
            escaped = value.replace("'", "''")
            return f"'{escaped}'"
        if isinstance(value, list):
            rendered_values = ", ".join(self._render_literal(item) for item in value)
            return f"({rendered_values})"
        raise TypeError(f"Unsupported literal value: {value!r}")

    def _add_days_expression(
        self,
        expression: str,
        days: int,
        dialect: str,
        *,
        cast_to_date: bool = False,
    ) -> str:
        if dialect == "mysql":
            return f"DATE_ADD({expression}, INTERVAL {days} DAY)"
        base_expression = f"({expression} + INTERVAL '{days} day')"
        if cast_to_date:
            return f"{base_expression}::date"
        return base_expression

    def _add_years_expression(self, expression: str, years: int, dialect: str) -> str:
        if dialect == "mysql":
            return f"DATE_ADD({expression}, INTERVAL {years} YEAR)"
        return f"({expression} + INTERVAL '{years} year')::date"
