from app.services.triage import triage


def test_negative_inventory_requires_human_review():
    source, result = triage("negative_inventory", "critical", -12)
    assert source == "rules"
    assert result.confidence == 1.0
    assert result.requires_human_review is True


def test_shortage_uses_mock_ai_path():
    source, result = triage("shortage", "high", -8)
    assert source == "mock_ai"
    assert result.classification == "warehouse_shortage"
