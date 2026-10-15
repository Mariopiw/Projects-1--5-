from app.schemas import AIClassification


def triage(exception_type: str, severity: str, difference: int) -> tuple[str, AIClassification]:
    if exception_type == "negative_inventory":
        return "rules", AIClassification(
            classification="negative_inventory",
            confidence=1.0,
            recommended_action="Verify inventory transactions before any adjustment.",
            requires_human_review=True,
        )
    if exception_type == "overstock":
        return "rules", AIClassification(
            classification="overstock",
            confidence=0.95,
            recommended_action="Verify receiving history and duplicate receipt possibility.",
            requires_human_review=True,
        )
    if exception_type == "shortage":
        confidence = 0.92 if abs(difference) >= 5 else 0.82
        return "mock_ai", AIClassification(
            classification="warehouse_shortage",
            confidence=confidence,
            recommended_action="Check recent receiving, picking, and return transactions.",
            requires_human_review=True,
        )
    return "fallback", AIClassification(
        classification="unknown",
        confidence=0.0,
        recommended_action="Route to manual review.",
        requires_human_review=True,
    )
