from __future__ import annotations

from datetime import date, datetime, timedelta
import re
from typing import Any

try:
    import pyperclip
except ImportError:  # pragma: no cover
    pyperclip = None

import streamlit as st

from core import GenerationRequest, SQLGenerator, ValidationError


ANALYSES = {
    "trend": {"label": "趋势分析", "summary": "按日、周、月生成趋势 SQL", "enabled": True},
    "compare": {"label": "同比 / 环比", "summary": "生成同比或环比 SQL", "enabled": True},
    "retention": {"label": "留存分析", "summary": "生成留存宽表或留存曲线 SQL", "enabled": True},
    "funnel": {"label": "漏斗分析", "summary": "按步骤漏斗生成转化 SQL", "enabled": True},
    "rfm": {"label": "RFM 分析", "summary": "生成人群分层与评分 SQL", "enabled": True},
}
UI_ANALYSES = ("trend", "compare", "retention", "funnel", "rfm")
DIALECTS = {"mysql": "MySQL", "postgresql": "PostgreSQL"}
AGGREGATIONS = ["sum", "count", "avg", "min", "max", "count_distinct"]
GRANULARITIES = ["day", "week", "month"]
COMPARISONS = {"mom": "环比", "yoy": "同比"}
RETENTION_MODES = {"table": "留存宽表", "curve": "留存曲线"}
FILTER_OPERATORS = ["=", "!=", ">", ">=", "<", "<=", "IN", "LIKE"]
DEFAULT_RETENTION_DAYS = [1, 3, 7, 14, 30]
INT_PATTERN = re.compile(r"^-?\d+$")
FLOAT_PATTERN = re.compile(r"^-?\d+\.\d+$")

EXAMPLES: dict[str, dict[str, Any]] = {
    "trend": {
        "dialect": "mysql",
        "parameters": {
            "table_name": "user_orders",
            "date_field": "order_date",
            "metric_field": "amount",
            "aggregation": "sum",
            "granularity": "day",
            "date_range": {"start": "2026-03-01", "end": "2026-03-31"},
            "filter_conditions": [{"field": "channel", "operator": "IN", "value": ["organic", "ads"]}],
        },
    },
    "compare": {
        "dialect": "postgresql",
        "parameters": {
            "table_name": "user_orders",
            "date_field": "order_date",
            "metric_field": "amount",
            "aggregation": "sum",
            "granularity": "month",
            "comparison_type": "yoy",
            "date_range": {"start": "2025-01-01", "end": "2026-03-31"},
            "filter_conditions": [{"field": "region", "operator": "=", "value": "APAC"}],
        },
    },
    "retention": {
        "dialect": "mysql",
        "parameters": {
            "table_name": "user_events",
            "user_id_field": "user_id",
            "date_field": "event_time",
            "retention_days": [1, 3, 7, 14, 30],
            "retention_mode": "curve",
            "start_date": "2026-02-01",
            "end_date": "2026-03-31",
            "filter_conditions": [{"field": "platform", "operator": "IN", "value": ["ios", "android"]}],
        },
    },
    "funnel": {
        "dialect": "mysql",
        "parameters": {
            "table_name": "user_events",
            "user_id_field": "user_id",
            "date_field": "event_time",
            "window_days": 7,
            "date_range": {"start": "2026-03-01", "end": "2026-03-31"},
            "steps": [
                {"step_name": "view_product", "filter_conditions": [{"field": "event_name", "operator": "=", "value": "view_product"}]},
                {"step_name": "add_to_cart", "filter_conditions": [{"field": "event_name", "operator": "=", "value": "add_to_cart"}]},
                {"step_name": "purchase", "filter_conditions": [{"field": "event_name", "operator": "=", "value": "purchase"}]},
            ],
        },
    },
    "rfm": {
        "dialect": "postgresql",
        "parameters": {
            "table_name": "user_orders",
            "user_id_field": "user_id",
            "date_field": "order_date",
            "amount_field": "amount",
            "analysis_date": "2026-03-31",
            "r_bins": 4,
            "f_bins": 4,
            "m_bins": 3,
            "filter_conditions": [{"field": "region", "operator": "=", "value": "APAC"}],
        },
    },
}


@st.cache_resource
def get_generator() -> SQLGenerator:
    return SQLGenerator()


def init_state() -> None:
    today = date.today()
    defaults: dict[str, Any] = {
        "selected_analysis": "trend",
        "selected_dialect": "mysql",
        "history": [],
        "current_result": None,
        "generation_error": None,
        "trend_table_name": "user_orders",
        "trend_date_field": "order_date",
        "trend_metric_field": "amount",
        "trend_aggregation": "sum",
        "trend_granularity": "day",
        "trend_date_range": (today - timedelta(days=30), today),
        "compare_table_name": "user_orders",
        "compare_date_field": "order_date",
        "compare_metric_field": "amount",
        "compare_aggregation": "sum",
        "compare_granularity": "month",
        "compare_comparison_type": "mom",
        "compare_date_range": (today - timedelta(days=180), today),
        "retention_table_name": "user_events",
        "retention_user_id_field": "user_id",
        "retention_date_field": "event_time",
        "retention_days": list(DEFAULT_RETENTION_DAYS),
        "retention_mode": "table",
        "retention_activity_range": (today - timedelta(days=90), today),
        "funnel_table_name": "user_events",
        "funnel_user_id_field": "user_id",
        "funnel_date_field": "event_time",
        "funnel_window_days": 7,
        "funnel_date_range": (today - timedelta(days=30), today),
        "funnel_step_filter_field": "event_name",
        "rfm_table_name": "user_orders",
        "rfm_user_id_field": "user_id",
        "rfm_date_field": "order_date",
        "rfm_amount_field": "amount",
        "rfm_analysis_date": today,
        "rfm_r_bins": 5,
        "rfm_f_bins": 5,
        "rfm_m_bins": 5,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)
    for analysis in UI_ANALYSES:
        st.session_state.setdefault(f"{analysis}_filter_rows", [0])
        st.session_state.setdefault(f"{analysis}_next_filter_id", 1)
        for row_id in st.session_state[f"{analysis}_filter_rows"]:
            ensure_filter_defaults(analysis, row_id)
    st.session_state.setdefault("funnel_step_rows", [0, 1, 2])
    st.session_state.setdefault("funnel_next_step_id", 3)
    default_steps = [
        ("view_product", "view_product"),
        ("add_to_cart", "add_to_cart"),
        ("purchase", "purchase"),
    ]
    for row_id in st.session_state["funnel_step_rows"]:
        default_name, default_value = default_steps[row_id] if row_id < len(default_steps) else ("", "")
        ensure_funnel_step_defaults(row_id, default_name=default_name, default_value=default_value)


def ensure_filter_defaults(analysis: str, row_id: int) -> None:
    st.session_state.setdefault(f"{analysis}_filter_field_{row_id}", "")
    st.session_state.setdefault(f"{analysis}_filter_operator_{row_id}", "=")
    st.session_state.setdefault(f"{analysis}_filter_value_{row_id}", "")


def ensure_funnel_step_defaults(
    row_id: int,
    *,
    default_name: str = "",
    default_value: str = "",
) -> None:
    st.session_state.setdefault(f"funnel_step_name_{row_id}", default_name)
    st.session_state.setdefault(f"funnel_step_value_{row_id}", default_value)
    st.session_state.setdefault(f"funnel_step_table_name_{row_id}", "")
    st.session_state.setdefault(f"funnel_step_user_id_field_{row_id}", "")
    st.session_state.setdefault(f"funnel_step_date_field_{row_id}", "")


def add_filter_row(analysis: str) -> None:
    row_id = st.session_state[f"{analysis}_next_filter_id"]
    st.session_state[f"{analysis}_next_filter_id"] = row_id + 1
    st.session_state[f"{analysis}_filter_rows"] = [*st.session_state[f"{analysis}_filter_rows"], row_id]
    ensure_filter_defaults(analysis, row_id)


def remove_filter_row(analysis: str, row_id: int) -> None:
    rows = [item for item in st.session_state[f"{analysis}_filter_rows"] if item != row_id]
    if not rows:
        new_row_id = st.session_state[f"{analysis}_next_filter_id"]
        st.session_state[f"{analysis}_next_filter_id"] = new_row_id + 1
        st.session_state[f"{analysis}_filter_rows"] = [new_row_id]
        ensure_filter_defaults(analysis, new_row_id)
        return
    st.session_state[f"{analysis}_filter_rows"] = rows


def add_funnel_step_row() -> None:
    row_id = st.session_state["funnel_next_step_id"]
    st.session_state["funnel_next_step_id"] = row_id + 1
    st.session_state["funnel_step_rows"] = [*st.session_state["funnel_step_rows"], row_id]
    ensure_funnel_step_defaults(row_id)


def remove_funnel_step_row(row_id: int) -> None:
    rows = [item for item in st.session_state["funnel_step_rows"] if item != row_id]
    if len(rows) < 2:
        return
    st.session_state["funnel_step_rows"] = rows


def parse_iso_date(value: str | None) -> date | None:
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def stringify_value(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def parse_scalar(raw_value: str) -> Any:
    value = raw_value.strip()
    if not value:
        raise ValueError("筛选条件值不能为空。")
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered == "null":
        return None
    if INT_PATTERN.fullmatch(value):
        return int(value)
    if FLOAT_PATTERN.fullmatch(value):
        return float(value)
    if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
        return value[1:-1]
    return value


def parse_date_range(value: Any) -> tuple[str | None, str | None]:
    if isinstance(value, (list, tuple)) and len(value) == 2 and all(isinstance(item, date) for item in value):
        start_date, end_date = value
        return start_date.isoformat(), end_date.isoformat()
    return None, None


def collect_filters(analysis: str) -> list[dict[str, Any]]:
    conditions: list[dict[str, Any]] = []
    for index, row_id in enumerate(st.session_state[f"{analysis}_filter_rows"], start=1):
        field = st.session_state.get(f"{analysis}_filter_field_{row_id}", "").strip()
        operator = st.session_state.get(f"{analysis}_filter_operator_{row_id}", "=")
        raw_value = st.session_state.get(f"{analysis}_filter_value_{row_id}", "").strip()
        if not field and not raw_value:
            continue
        if not field or not raw_value:
            raise ValueError(f"筛选条件第 {index} 行请同时填写字段和值。")
        if operator == "IN":
            items = [item.strip() for item in raw_value.split(",") if item.strip()]
            if not items:
                raise ValueError(f"筛选条件第 {index} 行的 IN 值至少填写一个。")
            value: Any = [parse_scalar(item) for item in items]
        elif operator == "LIKE":
            value = raw_value
        else:
            value = parse_scalar(raw_value)
        conditions.append({"field": field, "operator": operator, "value": value})
    return conditions


def apply_filters(analysis: str, filters: list[dict[str, Any]] | None) -> None:
    values = filters or []
    row_ids = list(range(len(values))) if values else [0]
    st.session_state[f"{analysis}_filter_rows"] = row_ids
    st.session_state[f"{analysis}_next_filter_id"] = len(row_ids)
    for row_id in row_ids:
        ensure_filter_defaults(analysis, row_id)
    if not values:
        st.session_state[f"{analysis}_filter_field_0"] = ""
        st.session_state[f"{analysis}_filter_operator_0"] = "="
        st.session_state[f"{analysis}_filter_value_0"] = ""
        return
    for row_id, condition in enumerate(values):
        st.session_state[f"{analysis}_filter_field_{row_id}"] = condition["field"]
        st.session_state[f"{analysis}_filter_operator_{row_id}"] = condition["operator"]
        st.session_state[f"{analysis}_filter_value_{row_id}"] = stringify_value(condition["value"])


def collect_funnel_steps() -> list[dict[str, Any]]:
    steps: list[dict[str, Any]] = []
    step_filter_field = st.session_state["funnel_step_filter_field"].strip()
    for index, row_id in enumerate(st.session_state["funnel_step_rows"], start=1):
        step_name = st.session_state.get(f"funnel_step_name_{row_id}", "").strip()
        step_value = st.session_state.get(f"funnel_step_value_{row_id}", "").strip()
        step_table_name = st.session_state.get(f"funnel_step_table_name_{row_id}", "").strip()
        step_user_id_field = st.session_state.get(f"funnel_step_user_id_field_{row_id}", "").strip()
        step_date_field = st.session_state.get(f"funnel_step_date_field_{row_id}", "").strip()

        if not step_name and not step_value:
            continue
        if not step_name or not step_value:
            raise ValueError(f"漏斗步骤第 {index} 行请同时填写步骤名称和步骤值。")
        if not step_filter_field:
            raise ValueError("请填写漏斗步骤筛选字段。")

        step: dict[str, Any] = {
            "step_name": step_name,
            "filter_conditions": [
                {
                    "field": step_filter_field,
                    "operator": "=",
                    "value": step_value,
                }
            ],
        }
        if step_table_name:
            step["table_name"] = step_table_name
        if step_user_id_field:
            step["user_id_field"] = step_user_id_field
        if step_date_field:
            step["date_field"] = step_date_field
        steps.append(step)
    return steps


def apply_funnel_steps(steps: list[dict[str, Any]] | None) -> None:
    normalized_steps = steps or []
    row_ids = list(range(len(normalized_steps))) if normalized_steps else [0, 1]
    st.session_state["funnel_step_rows"] = row_ids
    st.session_state["funnel_next_step_id"] = len(row_ids)

    first_filter_field = "event_name"
    for step in normalized_steps:
        filter_conditions = step.get("filter_conditions", [])
        if filter_conditions:
            first_filter_field = filter_conditions[0]["field"]
            break
    st.session_state["funnel_step_filter_field"] = first_filter_field

    for row_id in row_ids:
        ensure_funnel_step_defaults(row_id)

    for row_id, step in enumerate(normalized_steps):
        st.session_state[f"funnel_step_name_{row_id}"] = step["step_name"]
        filter_conditions = step.get("filter_conditions", [])
        st.session_state[f"funnel_step_value_{row_id}"] = (
            stringify_value(filter_conditions[0]["value"]) if filter_conditions else ""
        )
        st.session_state[f"funnel_step_table_name_{row_id}"] = step.get("table_name", "")
        st.session_state[f"funnel_step_user_id_field_{row_id}"] = step.get("user_id_field", "")
        st.session_state[f"funnel_step_date_field_{row_id}"] = step.get("date_field", "")


def load_parameters(analysis: str, parameters: dict[str, Any], dialect: str) -> None:
    st.session_state["selected_analysis"] = analysis
    st.session_state["selected_dialect"] = dialect
    if analysis == "trend":
        st.session_state["trend_table_name"] = parameters.get("table_name", "")
        st.session_state["trend_date_field"] = parameters.get("date_field", "")
        st.session_state["trend_metric_field"] = parameters.get("metric_field", "")
        st.session_state["trend_aggregation"] = parameters.get("aggregation", "sum")
        st.session_state["trend_granularity"] = parameters.get("granularity", "day")
        if date_range := parameters.get("date_range"):
            st.session_state["trend_date_range"] = (parse_iso_date(date_range["start"]), parse_iso_date(date_range["end"]))
        apply_filters("trend", parameters.get("filter_conditions"))
    elif analysis == "compare":
        st.session_state["compare_table_name"] = parameters.get("table_name", "")
        st.session_state["compare_date_field"] = parameters.get("date_field", "")
        st.session_state["compare_metric_field"] = parameters.get("metric_field", "")
        st.session_state["compare_aggregation"] = parameters.get("aggregation", "sum")
        st.session_state["compare_granularity"] = parameters.get("granularity", "month")
        st.session_state["compare_comparison_type"] = parameters.get("comparison_type", "mom")
        if date_range := parameters.get("date_range"):
            st.session_state["compare_date_range"] = (parse_iso_date(date_range["start"]), parse_iso_date(date_range["end"]))
        apply_filters("compare", parameters.get("filter_conditions"))
    elif analysis == "retention":
        st.session_state["retention_table_name"] = parameters.get("table_name", "")
        st.session_state["retention_user_id_field"] = parameters.get("user_id_field", "")
        st.session_state["retention_date_field"] = parameters.get("date_field", "")
        st.session_state["retention_days"] = parameters.get("retention_days", list(DEFAULT_RETENTION_DAYS))
        st.session_state["retention_mode"] = parameters.get("retention_mode", "table")
        start_date = parse_iso_date(parameters.get("start_date")) or (date.today() - timedelta(days=90))
        end_date = parse_iso_date(parameters.get("end_date")) or date.today()
        st.session_state["retention_activity_range"] = (start_date, end_date)
        apply_filters("retention", parameters.get("filter_conditions"))
    elif analysis == "funnel":
        st.session_state["funnel_table_name"] = parameters.get("table_name", "")
        st.session_state["funnel_user_id_field"] = parameters.get("user_id_field", "")
        st.session_state["funnel_date_field"] = parameters.get("date_field", "")
        st.session_state["funnel_window_days"] = parameters.get("window_days", 7)
        if date_range := parameters.get("date_range"):
            st.session_state["funnel_date_range"] = (
                parse_iso_date(date_range["start"]),
                parse_iso_date(date_range["end"]),
            )
        apply_filters("funnel", parameters.get("filter_conditions"))
        apply_funnel_steps(parameters.get("steps"))
    elif analysis == "rfm":
        st.session_state["rfm_table_name"] = parameters.get("table_name", "")
        st.session_state["rfm_user_id_field"] = parameters.get("user_id_field", "")
        st.session_state["rfm_date_field"] = parameters.get("date_field", "")
        st.session_state["rfm_amount_field"] = parameters.get("amount_field", "")
        st.session_state["rfm_analysis_date"] = parse_iso_date(parameters.get("analysis_date")) or date.today()
        st.session_state["rfm_r_bins"] = parameters.get("r_bins", 5)
        st.session_state["rfm_f_bins"] = parameters.get("f_bins", 5)
        st.session_state["rfm_m_bins"] = parameters.get("m_bins", 5)
        apply_filters("rfm", parameters.get("filter_conditions"))


def collect_parameters(analysis: str) -> dict[str, Any]:
    if analysis == "trend":
        start_date, end_date = parse_date_range(st.session_state["trend_date_range"])
        payload: dict[str, Any] = {
            "table_name": st.session_state["trend_table_name"].strip(),
            "date_field": st.session_state["trend_date_field"].strip(),
            "metric_field": st.session_state["trend_metric_field"].strip(),
            "aggregation": st.session_state["trend_aggregation"],
            "granularity": st.session_state["trend_granularity"],
            "filter_conditions": collect_filters("trend"),
        }
        if start_date and end_date:
            payload["date_range"] = {"start": start_date, "end": end_date}
        return payload
    if analysis == "compare":
        start_date, end_date = parse_date_range(st.session_state["compare_date_range"])
        payload = {
            "table_name": st.session_state["compare_table_name"].strip(),
            "date_field": st.session_state["compare_date_field"].strip(),
            "metric_field": st.session_state["compare_metric_field"].strip(),
            "aggregation": st.session_state["compare_aggregation"],
            "granularity": st.session_state["compare_granularity"],
            "comparison_type": st.session_state["compare_comparison_type"],
            "filter_conditions": collect_filters("compare"),
        }
        if start_date and end_date:
            payload["date_range"] = {"start": start_date, "end": end_date}
        return payload
    if analysis == "retention":
        start_date, end_date = parse_date_range(st.session_state["retention_activity_range"])
        payload = {
            "table_name": st.session_state["retention_table_name"].strip(),
            "user_id_field": st.session_state["retention_user_id_field"].strip(),
            "date_field": st.session_state["retention_date_field"].strip(),
            "retention_days": list(st.session_state["retention_days"]),
            "retention_mode": st.session_state["retention_mode"],
            "filter_conditions": collect_filters("retention"),
        }
        if start_date:
            payload["start_date"] = start_date
        if end_date:
            payload["end_date"] = end_date
        return payload
    if analysis == "funnel":
        start_date, end_date = parse_date_range(st.session_state["funnel_date_range"])
        payload = {
            "table_name": st.session_state["funnel_table_name"].strip(),
            "user_id_field": st.session_state["funnel_user_id_field"].strip(),
            "date_field": st.session_state["funnel_date_field"].strip(),
            "window_days": st.session_state["funnel_window_days"],
            "filter_conditions": collect_filters("funnel"),
            "steps": collect_funnel_steps(),
        }
        if start_date and end_date:
            payload["date_range"] = {"start": start_date, "end": end_date}
        return payload
    if analysis == "rfm":
        analysis_date = st.session_state["rfm_analysis_date"]
        payload = {
            "table_name": st.session_state["rfm_table_name"].strip(),
            "user_id_field": st.session_state["rfm_user_id_field"].strip(),
            "date_field": st.session_state["rfm_date_field"].strip(),
            "amount_field": st.session_state["rfm_amount_field"].strip(),
            "analysis_date": analysis_date.isoformat() if isinstance(analysis_date, date) else "",
            "r_bins": st.session_state["rfm_r_bins"],
            "f_bins": st.session_state["rfm_f_bins"],
            "m_bins": st.session_state["rfm_m_bins"],
            "filter_conditions": collect_filters("rfm"),
        }
        return payload
    return {}


def validate_form(analysis: str, parameters: dict[str, Any]) -> list[str]:
    if analysis not in UI_ANALYSES:
        return ["当前分析类型将在下一轮接入，本轮先开放趋势、同比/环比、留存分析。"]
    required = {
        "trend": ["table_name", "date_field", "metric_field", "granularity"],
        "compare": ["table_name", "date_field", "metric_field", "granularity", "comparison_type"],
        "retention": ["table_name", "user_id_field", "date_field", "retention_mode"],
        "funnel": ["table_name", "user_id_field", "date_field", "steps"],
        "rfm": ["table_name", "user_id_field", "date_field", "amount_field", "analysis_date"],
    }
    labels = {
        "table_name": "表名",
        "date_field": "日期字段",
        "metric_field": "指标字段",
        "granularity": "时间粒度",
        "comparison_type": "对比类型",
        "user_id_field": "用户 ID 字段",
        "retention_mode": "留存模式",
        "steps": "漏斗步骤",
        "amount_field": "金额字段",
        "analysis_date": "分析日期",
    }
    issues: list[str] = []
    for field in required.get(analysis, []):
        value = parameters.get(field)
        if isinstance(value, str) and not value.strip():
            issues.append(f"{labels[field]}不能为空。")
        elif value in (None, [], {}):
            issues.append(f"{labels[field]}不能为空。")
    if analysis in {"trend", "compare"} and "date_range" not in parameters:
        issues.append("请选择完整日期范围。")
    if analysis == "retention" and not parameters.get("retention_days"):
        issues.append("请至少选择一个留存天数。")
    if analysis == "funnel":
        if len(parameters.get("steps", [])) < 2:
            issues.append("请至少填写两个漏斗步骤。")
        if not st.session_state["funnel_step_filter_field"].strip():
            issues.append("请填写漏斗步骤筛选字段。")
    return issues


def copy_sql(sql: str) -> None:
    if pyperclip is None:
        st.warning("当前环境未安装 pyperclip，请使用代码块右上角复制按钮。")
        return
    try:
        pyperclip.copy(sql)
    except pyperclip.PyperclipException:
        st.warning("系统剪贴板暂不可用，请使用代码块右上角复制按钮。")
        return
    st.toast("SQL 已复制到剪贴板", icon=":material/content_copy:")


def build_result(analysis: str, dialect: str, parameters: dict[str, Any], sql: str) -> dict[str, Any]:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_tag = datetime.now().strftime("%Y%m%d_%H%M%S")
    return {
        "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "analysis": analysis,
        "dialect": dialect,
        "parameters": parameters,
        "created_at": timestamp,
        "outputs": [{"label": "主 SQL", "content": sql, "filename": f"{analysis}_{dialect}_{file_tag}.sql"}],
    }


def push_history(entry: dict[str, Any]) -> None:
    history = [item for item in st.session_state["history"] if item["id"] != entry["id"]]
    st.session_state["history"] = [entry, *history][:8]


def clear_current_result() -> None:
    st.session_state["current_result"] = None


def load_example(analysis: str) -> None:
    example = EXAMPLES[analysis]
    load_parameters(analysis, example["parameters"], example["dialect"])
    st.session_state["generation_error"] = None


def restore_history(entry_id: str) -> None:
    for entry in st.session_state["history"]:
        if entry["id"] == entry_id:
            st.session_state["current_result"] = entry
            load_parameters(entry["analysis"], entry["parameters"], entry["dialect"])
            st.session_state["generation_error"] = None
            return


def handle_generate() -> None:
    analysis = st.session_state["selected_analysis"]
    dialect = st.session_state["selected_dialect"]
    st.session_state["generation_error"] = None
    clear_current_result()

    try:
        parameters = collect_parameters(analysis)
    except ValueError as exc:
        st.session_state["generation_error"] = str(exc)
        return

    issues = validate_form(analysis, parameters)
    if issues:
        st.session_state["generation_error"] = "\n".join(issues)
        return

    try:
        sql = get_generator().generate(
            GenerationRequest(
                analysis_type=analysis,
                dialect=dialect,
                parameters=parameters,
            )
        )
    except ValidationError as exc:
        st.session_state["generation_error"] = str(exc)
        return

    result = build_result(analysis, dialect, parameters, sql)
    st.session_state["current_result"] = result
    push_history(result)


def render_filters(analysis: str) -> None:
    with st.expander("筛选条件（可选）", expanded=False, icon=":material/filter_list:"):
        st.caption("支持 =、!=、IN、LIKE。IN 请用英文逗号分隔多个值；数字、true/false/null 会自动识别。")
        for index, row_id in enumerate(st.session_state[f"{analysis}_filter_rows"], start=1):
            ensure_filter_defaults(analysis, row_id)
            field_col, operator_col, value_col, action_col = st.columns([1.2, 0.9, 1.4, 0.5])
            field_col.text_input(f"字段 {index}", key=f"{analysis}_filter_field_{row_id}", label_visibility="collapsed", placeholder="字段名")
            operator_col.selectbox(f"操作符 {index}", FILTER_OPERATORS, key=f"{analysis}_filter_operator_{row_id}", label_visibility="collapsed")
            value_col.text_input(f"值 {index}", key=f"{analysis}_filter_value_{row_id}", label_visibility="collapsed", placeholder="值 / 多值请用逗号分隔")
            action_col.button("删除", key=f"{analysis}_remove_filter_{row_id}", use_container_width=True, on_click=remove_filter_row, args=(analysis, row_id))
        st.button("新增筛选条件", key=f"{analysis}_add_filter", icon=":material/add:", on_click=add_filter_row, args=(analysis,))


def render_funnel_steps() -> None:
    with st.expander("漏斗步骤", expanded=True, icon=":material/stairs:"):
        st.caption("第一轮前端按“单事件表 + 每步一个主条件值”开放，实际会映射到 step.filter_conditions。")
        st.text_input("步骤筛选字段", key="funnel_step_filter_field", placeholder="例如 event_name")
        step_rows = st.session_state["funnel_step_rows"]
        can_remove = len(step_rows) > 2
        for index, row_id in enumerate(step_rows, start=1):
            ensure_funnel_step_defaults(row_id)
            with st.container(border=True):
                st.markdown(f"**步骤 {index}**")
                left, right = st.columns(2)
                left.text_input("步骤名称", key=f"funnel_step_name_{row_id}", placeholder="例如 purchase")
                right.text_input("步骤值", key=f"funnel_step_value_{row_id}", placeholder="例如 purchase")
                with st.expander("字段覆盖（可选）", expanded=False):
                    override_cols = st.columns(3)
                    override_cols[0].text_input("表名覆盖", key=f"funnel_step_table_name_{row_id}", placeholder="默认沿用顶层表名")
                    override_cols[1].text_input("用户字段覆盖", key=f"funnel_step_user_id_field_{row_id}", placeholder="默认沿用顶层用户字段")
                    override_cols[2].text_input("日期字段覆盖", key=f"funnel_step_date_field_{row_id}", placeholder="默认沿用顶层日期字段")
                st.button(
                    "删除该步骤",
                    key=f"funnel_remove_step_{row_id}",
                    use_container_width=True,
                    disabled=not can_remove,
                    on_click=remove_funnel_step_row,
                    args=(row_id,),
                )
        st.button("新增步骤", key="funnel_add_step", icon=":material/add:", on_click=add_funnel_step_row)


def summarize_parameters(analysis: str, parameters: dict[str, Any]) -> str:
    filter_count = len(parameters.get("filter_conditions", []))
    if analysis == "retention":
        return "\n".join([
            f"- 表名：`{parameters['table_name']}`",
            f"- 用户字段：`{parameters['user_id_field']}`",
            f"- 留存模式：`{parameters['retention_mode']}`",
            f"- 留存天数：`{', '.join(str(day) for day in parameters['retention_days'])}`",
            f"- 活跃范围：`{parameters.get('start_date', '未设置')} ~ {parameters.get('end_date', '未设置')}`",
            f"- 筛选条件：`{filter_count}` 条",
        ])
    if analysis == "funnel":
        date_range = parameters.get("date_range", {})
        step_names = ", ".join(step["step_name"] for step in parameters["steps"])
        return "\n".join([
            f"- 表名：`{parameters['table_name']}`",
            f"- 用户字段：`{parameters['user_id_field']}`",
            f"- 日期字段：`{parameters['date_field']}`",
            f"- 转化窗口：`{parameters['window_days']}` 天",
            f"- 步骤：`{step_names}`",
            f"- 日期范围：`{date_range.get('start', '未设置')} ~ {date_range.get('end', '未设置')}`",
            f"- 顶层筛选条件：`{filter_count}` 条",
        ])
    if analysis == "rfm":
        return "\n".join([
            f"- 表名：`{parameters['table_name']}`",
            f"- 用户字段：`{parameters['user_id_field']}`",
            f"- 日期字段：`{parameters['date_field']}`",
            f"- 金额字段：`{parameters['amount_field']}`",
            f"- 分析日期：`{parameters['analysis_date']}`",
            f"- 分箱：`R={parameters['r_bins']}, F={parameters['f_bins']}, M={parameters['m_bins']}`",
            f"- 筛选条件：`{filter_count}` 条",
        ])
    date_range = parameters.get("date_range", {})
    lines = [
        f"- 表名：`{parameters['table_name']}`",
        f"- 指标字段：`{parameters['metric_field']}`",
        f"- 时间粒度：`{parameters['granularity']}`",
        f"- 日期范围：`{date_range.get('start', '未设置')} ~ {date_range.get('end', '未设置')}`",
        f"- 筛选条件：`{filter_count}` 条",
    ]
    if analysis == "compare":
        lines.insert(3, f"- 对比类型：`{parameters['comparison_type']}`")
    else:
        lines.insert(3, f"- 聚合方式：`{parameters['aggregation']}`")
    return "\n".join(lines)


def main() -> None:
    st.set_page_config(page_title="SQL 分析模板生成器", page_icon=":material/query_stats:", layout="wide")
    init_state()

    with st.sidebar:
        st.markdown(":material/dashboard: **配置面板**")
        analysis = st.radio("分析类型", options=list(ANALYSES), format_func=lambda key: ANALYSES[key]["label"], key="selected_analysis")
        dialect = st.selectbox("SQL 方言", options=list(DIALECTS), format_func=lambda key: DIALECTS[key], key="selected_dialect")
        st.space("small")
        st.markdown(":material/rocket_launch: **快速示例**")
        for example_analysis in UI_ANALYSES:
            st.button(f"加载{ANALYSES[example_analysis]['label']}示例", key=f"example_{example_analysis}", use_container_width=True, on_click=load_example, args=(example_analysis,))
        st.space("small")
        st.markdown(":material/history: **会话历史**")
        if st.session_state["history"]:
            for entry in st.session_state["history"]:
                label = f"{ANALYSES[entry['analysis']]['label']} · {entry['created_at'][11:16]}"
                st.button(label, key=f"history_{entry['id']}", use_container_width=True, on_click=restore_history, args=(entry["id"],))
            st.button("清空历史", key="clear_history", use_container_width=True, on_click=lambda: st.session_state.update({"history": []}))
        else:
            st.caption("当前会话还没有历史记录。")
        st.space("small")
        st.markdown(":material/flag: **本轮范围**")
        st.markdown("- 已开放：趋势、同比/环比、留存、漏斗、RFM\n- 当前状态：完整版本五类分析均可生成 SQL")

    st.title("SQL 分析模板生成器", anchor=False)
    st.caption("把趋势、同比/环比、留存分析的真实 SQL 生成能力，升级为可输入、可生成、可展示、可复制下载的演示入口。")

    hero_left, hero_right = st.columns([1.6, 1])
    with hero_left.container(border=True):
        st.markdown(":blue-badge[Phase 3] :green-badge[真实生成链路] :orange-badge[会话内历史]")
        st.write("在左侧选择分析类型与 SQL 方言，在主区域填写参数后即可通过统一入口 `SQLGenerator` 生成 SQL，并完成复制、下载和历史回看。")
        if st.session_state["current_result"] is None:
            st.info("首次进入建议先加载一个示例，快速确认参数结构和输出格式。", icon=":material/lightbulb:")
    with hero_right.container(border=True):
        st.metric("已开放分析", "5 / 5")
        st.metric("当前方言", DIALECTS[dialect])
        st.metric("历史记录", len(st.session_state["history"]))

    form_col, result_col = st.columns([1.05, 1], gap="large")
    with form_col:
        st.markdown(f"**{ANALYSES[analysis]['label']}**")
        st.caption(ANALYSES[analysis]["summary"])
        if analysis == "trend":
            with st.container(border=True):
                left, right = st.columns(2)
                left.text_input("表名", key="trend_table_name", placeholder="例如 user_orders")
                right.text_input("日期字段", key="trend_date_field", placeholder="例如 order_date")
                left.text_input("指标字段", key="trend_metric_field", placeholder="例如 amount")
                right.selectbox("聚合方式", AGGREGATIONS, key="trend_aggregation")
                left.segmented_control("时间粒度", GRANULARITIES, key="trend_granularity", selection_mode="single")
                right.date_input("日期范围", key="trend_date_range")
                render_filters("trend")
        elif analysis == "compare":
            with st.container(border=True):
                left, right = st.columns(2)
                left.text_input("表名", key="compare_table_name", placeholder="例如 user_orders")
                right.text_input("日期字段", key="compare_date_field", placeholder="例如 order_date")
                left.text_input("指标字段", key="compare_metric_field", placeholder="例如 amount")
                right.selectbox("聚合方式", AGGREGATIONS, key="compare_aggregation")
                left.segmented_control("时间粒度", GRANULARITIES, key="compare_granularity", selection_mode="single")
                right.segmented_control("对比类型", list(COMPARISONS), format_func=lambda key: COMPARISONS[key], key="compare_comparison_type", selection_mode="single")
                st.date_input("日期范围", key="compare_date_range")
                render_filters("compare")
        elif analysis == "retention":
            with st.container(border=True):
                left, right = st.columns(2)
                left.text_input("表名", key="retention_table_name", placeholder="例如 user_events")
                right.text_input("用户 ID 字段", key="retention_user_id_field", placeholder="例如 user_id")
                left.text_input("日期字段", key="retention_date_field", placeholder="例如 event_time")
                right.segmented_control("留存模式", list(RETENTION_MODES), format_func=lambda key: RETENTION_MODES[key], key="retention_mode", selection_mode="single")
                st.multiselect("留存天数", DEFAULT_RETENTION_DAYS, key="retention_days")
                st.date_input("活跃日期范围", key="retention_activity_range")
                render_filters("retention")
        elif analysis == "funnel":
            with st.container(border=True):
                top_left, top_right = st.columns(2)
                top_left.text_input("表名", key="funnel_table_name", placeholder="例如 user_events")
                top_right.text_input("用户 ID 字段", key="funnel_user_id_field", placeholder="例如 user_id")
                bottom_left, bottom_right = st.columns(2)
                bottom_left.text_input("日期字段", key="funnel_date_field", placeholder="例如 event_time")
                bottom_right.number_input("转化窗口（天）", min_value=1, step=1, key="funnel_window_days")
                st.date_input("日期范围（可选）", key="funnel_date_range")
                render_filters("funnel")
                render_funnel_steps()
        elif analysis == "rfm":
            with st.container(border=True):
                row_one = st.columns(2)
                row_one[0].text_input("表名", key="rfm_table_name", placeholder="例如 user_orders")
                row_one[1].text_input("用户 ID 字段", key="rfm_user_id_field", placeholder="例如 user_id")
                row_two = st.columns(2)
                row_two[0].text_input("日期字段", key="rfm_date_field", placeholder="例如 order_date")
                row_two[1].text_input("金额字段", key="rfm_amount_field", placeholder="例如 amount")
                row_three = st.columns(4)
                row_three[0].date_input("分析日期", key="rfm_analysis_date")
                row_three[1].selectbox("R 分箱", options=list(range(2, 8)), key="rfm_r_bins")
                row_three[2].selectbox("F 分箱", options=list(range(2, 8)), key="rfm_f_bins")
                row_three[3].selectbox("M 分箱", options=list(range(2, 8)), key="rfm_m_bins")
                render_filters("rfm")
        else:
            with st.container(border=True):
                st.info("当前分析类型未开放，请从左侧选择已支持的分析。", icon=":material/schedule:")

        generate_disabled = analysis not in UI_ANALYSES
        with st.container(horizontal=True, horizontal_alignment="distribute"):
            st.button(
                "生成 SQL",
                type="primary",
                use_container_width=True,
                disabled=generate_disabled,
                icon=":material/play_arrow:",
                on_click=handle_generate,
            )
            st.button(
                "加载当前分析示例",
                use_container_width=True,
                disabled=generate_disabled,
                icon=":material/auto_awesome:",
                on_click=load_example,
                args=(analysis,),
            )

    with result_col:
        with st.container(border=True):
            st.subheader("生成结果", anchor=False)
            if st.session_state.get("generation_error"):
                st.error(st.session_state["generation_error"], icon=":material/error:")
            result = st.session_state.get("current_result")
            if result is None:
                st.caption("还没有生成 SQL。可以先填写参数，或从侧边栏加载一个示例。")
            else:
                st.success(f"{ANALYSES[result['analysis']]['label']} SQL 已生成，时间：{result['created_at']}，方言：{DIALECTS[result['dialect']]}", icon=":material/check_circle:")
                tabs = st.tabs([item["label"] for item in result["outputs"]])
                for tab, output in zip(tabs, result["outputs"], strict=True):
                    with tab:
                        left, right = st.columns(2)
                        if left.button("复制 SQL", key=f"copy_{result['id']}_{output['label']}", use_container_width=True, icon=":material/content_copy:"):
                            copy_sql(output["content"])
                        right.download_button("下载 .sql", data=output["content"], file_name=output["filename"], mime="text/sql", key=f"download_{result['id']}_{output['label']}", use_container_width=True, icon=":material/download:")
                        st.code(output["content"], language="sql")
                        st.caption("如果系统剪贴板不可用，也可以使用代码块右上角复制按钮。")
                with st.expander("参数摘要", expanded=True, icon=":material/tune:"):
                    st.markdown(summarize_parameters(result["analysis"], result["parameters"]))


if __name__ == "__main__":
    main()
