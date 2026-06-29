from typing import Any, Dict, List
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class SMTEngine(MotorICT):
    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        asset1 = context.get('asset1_swings')
        asset2 = context.get('asset2_swings')
        if not asset1 or not asset2:
            return LayerOutput(
                id=f"smt_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name="SMTEngine",
                semantic_type="SMT", confidence=0.0, valid=False,
                evidence=["Dados de ambos ativos necessários"]
            )
        def last_extreme(swings, direction='high'):
            candidates = [s for s in swings if s['type'] == direction]
            return candidates[-1]['price'] if candidates else None
        a1_high = last_extreme(asset1, 'high')
        a2_high = last_extreme(asset2, 'high')
        a1_low = last_extreme(asset1, 'low')
        a2_low = last_extreme(asset2, 'low')
        divergent = False
        if a1_high and a2_high and a1_high > a2_high:
            divergent = True
        elif a1_low and a2_low and a1_low < a2_low:
            divergent = True
        return LayerOutput(
            id=f"smt_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="SMTEngine",
            semantic_type="SMT", confidence=0.8 if divergent else 0.3, valid=divergent,
            evidence=["SMT divergente" if divergent else "Sem divergência"],
            payload={"type": "divergent" if divergent else "convergent"}
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["SMTEngine compara estrutura entre ativos."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
