
from typing import Dict, List

def score_severity(rule: Dict) -> Dict:
    family = rule.get("rule_family") or rule.get("family")
    signals: List[str] = []
    level = "Low"
    rationale = []

    # Examples based on defaults: elevate for predictive scheduling & clopening risk
    if family in {"predictive_scheduling","clopening"}:
        level = "Medium"
        rationale.append("Scheduling changes and rest windows can cause recurring harms")
        signals.append("Statutory premiums for short-notice changes")
    if family in {"youth_labor"}:
        level = "Critical"
        rationale.append("Protected population (minors) and safety implications")
        signals.append("Child labor limits and penalties")

    # Escalation owner/SLA examples
    escalation = {"sla_hours": {"Critical":24,"High":72,"Medium":24*7,"Low":24*14}[level],
                  "owner": ["Scheduling","Payroll"] if level in {"High","Medium"} else ["Payroll","Compliance"]}

    return {
        "level": level,
        "rationale": "; ".join(rationale) or None,
        "signals": signals,
        "escalation": escalation
    }
