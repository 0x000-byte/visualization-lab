from typing import List
import pandas as pd
from .types import IntentNode, VizCandidateNode
from .parser_nl import parse_intent
from .candidates import generate_candidates
from .ranking import rank_candidates


class IntentManager:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.schema = list(df.columns)
        self.intents: List[IntentNode] = []
        self.candidates: List[VizCandidateNode] = []

    def parse(self, text: str) -> IntentNode:
        intent = parse_intent(text, self.schema)
        self.intents.append(intent)
        return intent

    def suggest(self, intent: IntentNode, top_k: int = 3) -> List[VizCandidateNode]:
        cands = generate_candidates(intent, self.df, max_k=10)
        ranked = rank_candidates(intent, cands, self.df)[:top_k]
        self.candidates.extend(ranked)
        return ranked

