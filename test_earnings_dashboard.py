import pytest
from datetime import datetime

from earnings_dashboard import WorkerEarningsDashboard


def test_add_earning_and_totals():
    dash = WorkerEarningsDashboard()
    dash.add_earning("w1", "Alice", 100.0, "Task A")
    dash.add_earning("w1", "Alice", 200.0, "Task B")
    dash.add_earning("w2", "Bob", 150.0, "Task C")

    assert dash.get_total_earnings("w1") == 300.0
    assert dash.get_total_earnings("w2") == 150.0


def test_top_earners():
    dash = WorkerEarningsDashboard()
    dash.add_earning("w1", "Alice", 100.0)
    dash.add_earning("w2", "Bob", 350.0)
    dash.add_earning("w3", "Carol", 200.0)

    top = dash.get_top_earners(2)
    assert top[0][0] == "w2"
    assert top[1][0] == "w3"


def test_monthly_totals():
    dash = WorkerEarningsDashboard()
    dash.add_earning("w1", "Alice", 100.0, timestamp=datetime(2026, 3, 1, 9, 0, 0))
    dash.add_earning("w1", "Alice", 200.0, timestamp=datetime(2026, 2, 15, 12, 0, 0))
    dash.add_earning("w2", "Bob", 50.0, timestamp=datetime(2026, 3, 20, 14, 0, 0))

    monthly = dash.get_monthly_totals(2026, 3)
    assert monthly["w1"] == 100.0
    assert monthly["w2"] == 50.0
    assert "w1" in monthly


def test_clear_resets_state():
    dash = WorkerEarningsDashboard()
    dash.add_earning("w1", "Alice", 100.0)
    dash.clear()
    assert dash.get_earnings("w1") == []


def test_negative_amount_raises_error():
    dash = WorkerEarningsDashboard()
    with pytest.raises(ValueError):
        dash.add_earning("w1", "Alice", -25.0)
