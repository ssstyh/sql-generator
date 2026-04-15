from app import build_result, parse_scalar, stringify_value, validate_form


def test_parse_scalar_normalizes_common_value_types() -> None:
    assert parse_scalar("42") == 42
    assert parse_scalar("3.14") == 3.14
    assert parse_scalar("true") is True
    assert parse_scalar("null") is None


def test_stringify_value_supports_lists_and_booleans() -> None:
    assert stringify_value(["ios", "android"]) == "ios, android"
    assert stringify_value(False) == "false"


def test_validate_form_flags_missing_required_fields() -> None:
    issues = validate_form(
        "trend",
        {
            "table_name": "",
            "date_field": "order_date",
            "metric_field": "amount",
            "granularity": "day",
        },
    )

    assert "表名不能为空。" in issues
    assert "请选择完整日期范围。" in issues


def test_build_result_includes_download_metadata() -> None:
    result = build_result(
        analysis="compare",
        dialect="mysql",
        parameters={"table_name": "user_orders"},
        sql="select 1;",
    )

    assert result["analysis"] == "compare"
    assert result["outputs"][0]["filename"].startswith("compare_mysql_")
    assert result["outputs"][0]["content"] == "select 1;"
