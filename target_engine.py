from typing import Any, Dict, List
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class TargetEngine(MotorICT):
    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        entry = context.get('entry')
        external_liq = context.get('external_liquidity')
        internal_liq = context.get('internal_liquidity')
        fvg = context.get('fvg')
        targets = []
        if internal_liq and internal_liq.valid:
            levels = internal_liq.payload.get('levels', [])
            if levels:
                targets.append({"type": "IRL", "price": levels[0].get('price')})
        if external_liq and external_liq.valid:
            side = 'buy_side_levels' if entry and entry.payload.get('direction') == 'sell' else 'sell_side_levels'
            levels = external_liq.payload.get(side, [])
            if levels:
                targets.append({"type": "ERL", "price": levels[0]['price']})
        if fvg and fvg.valid:
            targets.append({"type": "FVG", "price": fvg.payload.get('upper')})
        return LayerOutput(
            id=f"tgt_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="TargetEngine",
            semantic_type="TargetDelivery", confidence=0.8 if targets else 0.0,
            valid=bool(targets),
            evidence=[f"Alvos: {len(targets)}"],
            payload={"targets": targets}
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["TargetEngine calcula objetivos de saída."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
