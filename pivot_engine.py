from typing import Any, Dict, List
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class PivotEngine(MotorICT):
    def __init__(self, min_distance_pct: float = 0.002):
        self.min_distance_pct = min_distance_pct

    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        swings = context.get('swings', [])
        if not swings:
            return LayerOutput(
                id=f"pivot_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name="PivotEngine",
                semantic_type="Pivot", confidence=0.0, valid=False,
                evidence=["Nenhum swing fornecido"]
            )
        pivots = []
        last_price = None
        for s in swings:
            if last_price is None or abs(s['price'] - last_price) / last_price > self.min_distance_pct:
                pivots.append(s)
                last_price = s['price']
        return LayerOutput(
            id=f"pivot_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="PivotEngine",
            semantic_type="Pivot", confidence=1.0, valid=bool(pivots),
            evidence=[f"Pivots filtrados: {len(pivots)}"],
            payload={"pivots": pivots}
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["PivotEngine removeu swings irrelevantes próximos."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return {"pivots": output.payload.get('pivots')}
