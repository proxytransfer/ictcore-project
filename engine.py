from typing import List
from core.interfaces import InferenceEngine
from core.models import MarketEvent, SemanticEvent, Hypothesis
from ontology.graph import build_concept_graph

class ForwardChainingEngine(InferenceEngine):
    def __init__(self, rules: List[dict] = None):
        self.rules = rules or []
        self.graph = build_concept_graph()

    async def infer(self, semantic_events: List[SemanticEvent], market_events: List[MarketEvent]) -> List[Hypothesis]:
        hypotheses = []
        active_concepts = {ev.concept for ev in semantic_events}
        for rule in self.rules:
            if all(cond in active_concepts for cond in rule["if"]):
                conf = rule["confidence"] * min(
                    (ev.confidence for ev in semantic_events if ev.concept in rule["if"]),
                    default=1.0
                )
                hypotheses.append(Hypothesis(
                    statement=rule["then"],
                    confidence=conf,
                    supporting_events=[ev for ev in semantic_events if ev.concept in rule["if"]],
                    contradictory_events=[],
                    trace={"rule": rule, "active_concepts": list(active_concepts)}
                ))
        return hypotheses
