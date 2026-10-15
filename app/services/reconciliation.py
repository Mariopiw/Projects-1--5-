from dataclasses import dataclass


@dataclass(frozen=True)
class Classification:
    exception_type: str
    severity: str


def classify_difference(expected: int, actual: int) -> Classification:
    difference = actual - expected
    if actual < 0:
        return Classification("negative_inventory", "critical")
    if difference < 0:
        shortage = abs(difference)
        if shortage >= 10:
            return Classification("shortage", "critical")
        if shortage >= 5:
            return Classification("shortage", "high")
        return Classification("shortage", "medium")
    if difference > 0:
        return Classification("overstock", "low")
    return Classification("match", "none")
