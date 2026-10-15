from app.services.reconciliation import classify_difference


def test_match():
    result = classify_difference(10, 10)
    assert (result.exception_type, result.severity) == ("match", "none")


def test_shortage_levels():
    assert classify_difference(10, 8).severity == "medium"
    assert classify_difference(10, 5).severity == "high"
    assert classify_difference(20, 10).severity == "critical"


def test_negative_inventory():
    result = classify_difference(10, -1)
    assert result.exception_type == "negative_inventory"
    assert result.severity == "critical"
