from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import time
import uuid


class IntentType(str, Enum):
    DESCRIBE = "describe"
    COMPARE = "compare"


class NodeStatus(str, Enum):
    PROPOSED = "proposed"
    ACTIVE = "active"
    SATISFIED = "satisfied"
    OBSOLETE = "obsolete"


@dataclass
def _stamp() -> float:
    return time.time()


@dataclass
class IntentNode:
    id: str
    intent_type: IntentType
    targets: List[str] = field(default_factory=list)
    group_by: List[str] = field(default_factory=list)
    filters: Dict[str, Any] = field(default_factory=dict)
    time_context: Optional[Dict[str, str]] = None
    status: NodeStatus = NodeStatus.ACTIVE
    confidence: float = 0.6
    source: str = "nl_query"
    created_at: float = field(default_factory=_stamp)

    @staticmethod
    def new(**kw) -> "IntentNode":
        return IntentNode(id=str(uuid.uuid4()), **kw)


@dataclass
class VizCandidateNode:
    id: str
    intent_ids: List[str]
    spec: Dict[str, Any]  # keep generic; could be Vega-Lite later
    rationale: str = ""
    scoring: Dict[str, float] = field(default_factory=dict)
    confidence: float = 0.6
    risk_flags: List[str] = field(default_factory=list)

    @staticmethod
    def new(**kw) -> "VizCandidateNode":
        return VizCandidateNode(id=str(uuid.uuid4()), **kw)

