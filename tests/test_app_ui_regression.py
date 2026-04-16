from pathlib import Path
from streamlit.testing.v1 import AppTest


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


def make_app() -> AppTest:
    return AppTest.from_file(str(APP_PATH)).run()


def click_button(
    at: AppTest,
    *,
    label: str | None = None,
    key: str | None = None,
) -> AppTest:
    for button in at.button:
        if key is not None and button.key == key:
            return button.click().run()
        if label is not None and button.label == label:
            return button.click().run()
    raise AssertionError(f"Button not found: label={label!r}, key={key!r}")


def test_compare_example_loads_analysis_specific_state() -> None:
    at = make_app()

    at = click_button(at, key="example_compare")

    assert at.session_state["selected_analysis"] == "compare"
    assert at.session_state["selected_dialect"] == "postgresql"
    assert at.session_state["compare_table_name"] == "user_orders"
    assert at.session_state["compare_comparison_type"] == "yoy"
    assert at.session_state["compare_filter_field_0"] == "region"
    assert at.session_state["compare_filter_value_0"] == "APAC"


def test_sidebar_scope_copy_matches_opened_analyses() -> None:
    at = make_app()

    markdown_values = [markdown.value for markdown in at.markdown]

    assert any(
        "已开放：趋势、同比/环比、留存、漏斗、RFM" in value
        for value in markdown_values
    )
    assert not any("下一轮接入" in value for value in markdown_values)


def test_trend_generation_renders_sql_and_parameter_summary() -> None:
    at = make_app()

    at = click_button(at, label="生成 SQL")

    assert at.session_state["current_result"]["analysis"] == "trend"
    assert len(at.code) == 1
    assert "FROM user_orders" in at.code[0].value
    assert any("表名：`user_orders`" in markdown.value for markdown in at.markdown)
    assert len(at.session_state["history"]) == 1
    history_buttons = [button for button in at.button if (button.key or "").startswith("history_")]
    assert len(history_buttons) == 1
    assert history_buttons[0].label.startswith("趋势分析")


def test_history_restore_recovers_previous_generated_result() -> None:
    at = make_app()

    at = click_button(at, label="生成 SQL")
    at = at.sidebar.radio[0].set_value("trend").run()
    at = click_button(at, key="example_compare")
    at = click_button(at, label="生成 SQL")
    at = at.sidebar.radio[0].set_value("compare").run()

    history_buttons = [button for button in at.button if (button.key or "").startswith("history_")]

    assert len(history_buttons) == 2

    trend_history_button = next(
        button for button in history_buttons if button.label.startswith("趋势分析")
    )
    at = trend_history_button.click().run()

    assert at.session_state["selected_analysis"] == "trend"
    assert at.session_state["current_result"]["analysis"] == "trend"


def test_retention_requires_at_least_one_day_before_generation() -> None:
    at = make_app()

    at = at.sidebar.radio[0].set_value("retention").run()
    at = at.multiselect[0].set_value([]).run()
    at = click_button(at, label="生成 SQL")

    assert [error.value for error in at.error] == ["请至少选择一个留存天数。"]


def test_failed_generation_clears_previous_success_result() -> None:
    at = make_app()

    at = click_button(at, label="生成 SQL")
    at = next(widget for widget in at.text_input if widget.key == "trend_table_name").set_value("").run()
    at = click_button(at, label="生成 SQL")

    assert at.session_state["current_result"] is None
    assert [error.value for error in at.error] == ["表名不能为空。"]
    assert len(at.success) == 0
    assert len(at.code) == 0


def test_funnel_generation_renders_sql_and_summary() -> None:
    at = make_app()

    at = at.sidebar.radio[0].set_value("funnel").run()
    at = click_button(at, label="生成 SQL")

    assert at.session_state["current_result"]["analysis"] == "funnel"
    assert "STEP_ORDER" in at.code[0].value.upper()
    assert "CONVERSION_RATE" in at.code[0].value.upper()
    assert any("转化窗口：`7` 天" in markdown.value for markdown in at.markdown)


def test_rfm_generation_renders_sql_and_summary() -> None:
    at = make_app()

    at = at.sidebar.radio[0].set_value("rfm").run()
    at = click_button(at, label="生成 SQL")

    assert at.session_state["current_result"]["analysis"] == "rfm"
    assert "RFM_SCORE" in at.code[0].value.upper()
    assert "SEGMENT_LABEL" in at.code[0].value.upper()
    assert any("金额字段：`amount`" in markdown.value for markdown in at.markdown)
