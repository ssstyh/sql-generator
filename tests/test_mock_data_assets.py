from __future__ import annotations

import csv
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MOCK_DATA_DIR = PROJECT_ROOT / "mock_data"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").date()


def test_user_orders_mock_data_matches_current_examples() -> None:
    rows = read_csv_rows(MOCK_DATA_DIR / "user_orders.csv")

    assert rows
    assert list(rows[0]) == ["order_id", "user_id", "order_date", "amount", "channel", "region"]

    order_dates = [parse_date(row["order_date"]) for row in rows]
    assert min(order_dates) == date(2025, 1, 1)
    assert max(order_dates) == date(2026, 3, 31)

    channels = {row["channel"] for row in rows}
    assert {"organic", "ads", "email", "referral"} <= channels

    regions = {row["region"] for row in rows}
    assert {"APAC", "EMEA", "NA"} <= regions

    trend_dates = {
        parse_date(row["order_date"])
        for row in rows
        if row["channel"] in {"organic", "ads"} and date(2026, 3, 1) <= parse_date(row["order_date"]) <= date(2026, 3, 31)
    }
    assert len(trend_dates) == 31

    apac_months = {
        (parse_date(row["order_date"]).year, parse_date(row["order_date"]).month)
        for row in rows
        if row["region"] == "APAC"
    }
    assert {(2025, 1), (2025, 2), (2025, 3), (2026, 1), (2026, 2), (2026, 3)} <= apac_months


def test_user_events_mock_data_covers_retention_example_days() -> None:
    rows = read_csv_rows(MOCK_DATA_DIR / "user_events.csv")

    assert rows
    assert list(rows[0]) == ["event_id", "user_id", "event_time", "platform"]

    event_dates = [parse_date(row["event_time"]) for row in rows]
    assert min(event_dates) == date(2026, 2, 1)
    assert max(event_dates) == date(2026, 3, 31)

    platforms = {row["platform"] for row in rows}
    assert {"ios", "android", "web", "miniapp"} <= platforms

    activity_by_user: dict[str, list[date]] = defaultdict(list)
    for row in rows:
        if row["platform"] in {"ios", "android"}:
            activity_by_user[row["user_id"]].append(parse_date(row["event_time"]))

    covered_days = set()
    for activity_dates in activity_by_user.values():
        ordered_dates = sorted(set(activity_dates))
        cohort_date = ordered_dates[0]
        for activity_date in ordered_dates[1:]:
            covered_days.add((activity_date - cohort_date).days)

    assert {1, 3, 7, 14, 30} <= covered_days


def test_sql_assets_exist_for_mysql_and_postgresql() -> None:
    mysql_init = (MOCK_DATA_DIR / "mysql" / "init.sql").read_text(encoding="utf-8")
    postgresql_init = (MOCK_DATA_DIR / "postgresql" / "init.sql").read_text(encoding="utf-8")

    for content in (mysql_init, postgresql_init):
        assert "CREATE TABLE user_orders" in content
        assert "CREATE TABLE user_events" in content
        assert "INSERT INTO user_orders" in content
        assert "INSERT INTO user_events" in content

    trend_reference = (MOCK_DATA_DIR / "reference_sql" / "trend_example.mysql.sql").read_text(encoding="utf-8")
    compare_reference = (MOCK_DATA_DIR / "reference_sql" / "compare_example.postgresql.sql").read_text(encoding="utf-8")
    retention_reference = (MOCK_DATA_DIR / "reference_sql" / "retention_example.mysql.sql").read_text(encoding="utf-8")

    assert "period_start" in trend_reference
    assert "current_value" in compare_reference and "previous_value" in compare_reference
    assert "cohort_date" in retention_reference and "retention_day" in retention_reference
