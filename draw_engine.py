from typing import Any, Dict, List
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class DrawEngine(MotorICT):
    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        quarterly = context.get('quarterly')
        dealing_range = context.get('dealing_range')
        if not quarterly or not dealing_range or not quarterly.valid or not dealing_range.valid:
            return LayerOutput(
                id=f"draw_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name="DrawEngine",
                semantic_type="DrawOnLiquidity", confidence=0.0, valid=False,
                evidence=["Contexto trimestral ou dealing range ausente"]
            )
        bias = quarterly.payload.get('bias')
        if bias == 'bullish':
            direction = 'buy_side'
            level = dealing_range.payload['high']
        else:
            direction = 'sell_side'
            level = dealing_range.payload['low']
        return LayerOutput(
            id=f"draw_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="DrawEngine",
            semantic_type="DrawOnLiquidity", confidence=0.9, valid=True,
            evidence=[f"Draw on {direction} at {level}"],
            payload={"direction": direction, "level": level}
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["DrawEngine projeta o alvo de liquidez."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
