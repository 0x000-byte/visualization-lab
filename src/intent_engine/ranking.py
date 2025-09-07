from typing import List
import itertools
import numpy as np
import pandas as pd
from .types import VizCandidateNode, IntentNode, IntentType


def _effect_size_means(df: pd.DataFrame, group: str, y: str) -> float:
    # crude pooled Cohen's d average across pairs
    if group not in df or y not in df: return 0.0
    groups = [g for g, d in df.groupby(group) if len(d) > 1]
    if len(groups) < 2: return 0.0
    ds = []
    for a, b in itertools.combinations(groups, 2):
        da = df[df[group] == a][y].dropna()
        db = df[df[group] == b][y].dropna()
        if len(da) < 2 or len(db) < 2: 
            continue
        s_p = np.sqrt(((da.var(ddof=1)*(len(da)-1)) + (db.var(ddof=1)*(len(db)-1))) / (len(da)+len(db)-2))
        if s_p == 0: 
            continue
        d = abs(da.mean() - db.mean()) / s_p
        ds.append(d)
    return float(np.mean(ds)) if ds else 0.0


def rank_candidates(intent: IntentNode, candidates: List[VizCandidateNode], df: pd.DataFrame) -> List[VizCandidateNode]:
    ranked: List[VizCandidateNode] = []
    for c in candidates:
        score = 0.3  # base

        # crude IG proxy
        if intent.intent_type == IntentType.COMPARE and c.spec["type"] in ("bar_mean", "box", "diff_table"):
            y = intent.targets[0]
            g = intent.group_by[0]
            ig = _effect_size_means(df, g, y)  # ~ expected interestingness
            score += min(ig / 1.5, 0.6)  # cap
            c.scoring["IG_proxy"] = ig

        # clarity proxy
        clarity = 0.3
        if c.spec["type"] in ("summary", "bar_mean"):
            clarity = 0.5
        score += clarity
        c.scoring["clarity"] = clarity

        # tiny cognitive load penalty
        load = 0.0 if c.spec["type"] in ("summary", "bar_mean") else 0.1
        score -= load
        c.scoring["cog_load_penalty"] = load

        c.scoring["score"] = score
        ranked.append(c)

    ranked.sort(key=lambda x: x.scoring.get("score", 0), reverse=True)
    return ranked

