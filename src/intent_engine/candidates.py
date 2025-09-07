from typing import Any, Dict, List
import math
import numpy as np
import pandas as pd
from .types import IntentNode, IntentType, VizCandidateNode


def _cat_cardinality(df: pd.DataFrame, col: str) -> int:
    return int(df[col].nunique()) if col in df.columns else 0


def generate_candidates(intent: IntentNode, df: pd.DataFrame, max_k: int = 3) -> List[VizCandidateNode]:
    nodes: List[VizCandidateNode] = []

    if intent.intent_type == IntentType.DESCRIBE:
        target = intent.targets[0] if intent.targets else df.select_dtypes("number").columns[0]
        # Candidate 1: histogram
        nodes.append(VizCandidateNode.new(
            intent_ids=[intent.id],
            spec={"type": "histogram", "x": target, "bins": 30},
            rationale=f"Distribution of {target} (overview)."
        ))
        # Candidate 2: summary stats
        nodes.append(VizCandidateNode.new(
            intent_ids=[intent.id],
            spec={"type": "summary", "field": target},
            rationale=f"Summary stats for {target} (mean, std, quantiles)."
        ))

    elif intent.intent_type == IntentType.COMPARE:
        target = intent.targets[0] if intent.targets else df.select_dtypes("number").columns[0]
        group = intent.group_by[0] if intent.group_by else df.select_dtypes("object").columns[0]
        card = _cat_cardinality(df, group)
        # Candidate 1: mean bar
        nodes.append(VizCandidateNode.new(
            intent_ids=[intent.id],
            spec={"type": "bar_mean", "x": group, "y": target, "agg": "mean", "limit_topk": 20},
            rationale=f"Compare mean {target} across {group}."
        ))
        # Candidate 2: distribution box/violin if reasonable
        if card <= 15:
            nodes.append(VizCandidateNode.new(
                intent_ids=[intent.id],
                spec={"type": "box", "x": group, "y": target},
                rationale=f"Show distribution of {target} by {group} (shape & outliers)."
            ))
        # Candidate 3: difference table (effect sizes)
        nodes.append(VizCandidateNode.new(
            intent_ids=[intent.id],
            spec={"type": "diff_table", "group": group, "metric": target},
            rationale=f"Pairwise differences in {target} between {group} levels."
        ))

    return nodes[:max_k]

