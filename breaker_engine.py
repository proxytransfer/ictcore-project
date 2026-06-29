from typing import Any, Dict, List
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class BreakerEngine(MotorICT):
    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        order_block = context.get('order_block')
        mss = context.get('mss')
        if not order_block or not order_block.valid or not mss or not mss.valid:
            return LayerOutput(
                id=f"breaker_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name="BreakerEngine",
                semantic_type="Breaker", confidence=0.0, valid=False,
                evidence=["OB ou MSS ausentes"]
            )
        current_price = context.get('current_price', 0)
        ob_high = order_block.payload['high']
        ob_low = order_block.payload['low']
        if (order_block.payload['direction'] == 'bullish' and current_price < ob_low) or \
           (order_block.payload['direction'] == 'bearish' and current_price > ob_high):
            return LayerOutput(
                id=f"breaker_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name="BreakerEngine",
                semantic_type="Breaker", confidence=0.7, valid=True,
                evidence=["Breaker Block confirmado"],
                payload={"ob": order_block.payload, "broken": True}
            )
        return LayerOutput(
            id=f"breaker_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="BreakerEngine",
            semantic_type="Breaker", confidence=0.0, valid=False,
            evidence=["OB não rompido"]
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["BreakerEngine avalia rompimento de OBs."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
