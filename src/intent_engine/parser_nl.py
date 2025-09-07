import re
from typing import Dict, List, Optional
from .types import IntentNode, IntentType

# Ultra-light parser: looks for keywords & schema mentions.
def parse_intent(
    text: str,
    schema_columns: List[str],
    default_time_col: Optional[str] = None,
) -> IntentNode:
    t = text.lower()

    # intent type
    intent_type = IntentType.COMPARE if "compare" in t or "vs" in t else IntentType.DESCRIBE

    # crude target detection: first known metric mentioned
    metrics = [c for c in schema_columns if any(k in c.lower() for k in ["rev", "churn", "rate", "value", "score", "amount", "count"])]
    targets = []
    for m in metrics:
        if re.search(rf"\b{re.escape(m.lower())}\b", t):
            targets.append(m)
    if not targets and metrics:
        targets = [metrics[0]]

    # crude group-by detection
    group_by = []
    group_words = ["by", "across", "per"]
    if any(w in t for w in group_words):
        for c in schema_columns:
            if re.search(rf"\b{re.escape(c.lower())}\b", t):
                if c not in targets:
                    group_by.append(c)
    # common categorical fallbacks
    if not group_by:
        for cand in ["plan", "segment", "category"]:
            if cand in schema_columns:
                group_by = [cand]
                break

    # time window detection (very basic)
    time_context = None
    if "q2" in t:
        time_context = {"start": "2025-04-01", "end": "2025-06-30"}
    elif "q1" in t:
        time_context = {"start": "2025-01-01", "end": "2025-03-31"}

    return IntentNode.new(
        intent_type=intent_type,
        targets=targets,
        group_by=group_by if intent_type == IntentType.COMPARE else [],
        time_context=time_context,
        status="active",
        confidence=0.6,
        source="nl_query",
    )

