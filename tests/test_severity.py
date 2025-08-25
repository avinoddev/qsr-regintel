
from libs.severity.score import score_severity

def test_predictive_is_medium():
    rule = {"family":"predictive_scheduling"}
    s = score_severity(rule)
    assert s["level"] in {"Medium","High","Critical"}
