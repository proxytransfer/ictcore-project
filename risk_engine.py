from typing import Any, Dict, List
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class RiskEngine(MotorICT):
    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        entry_price = context.get('entry_price', 0)
        atr = context.get('atr', 0)
        direction = context.get('direction', 'buy')
        if entry_price <= 0 or atr <= 0:
            return LayerOutput(
                id=f"risk_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name="RiskEngine",
                semantic_type="Risk", confidence=0.0, valid=False,
                evidence=["Preço/ATR inválidos"]
            )
        multiplier = 1.5
        if direction == 'buy':
            stop = entry_price - multiplier * atr
            tp = entry_price + 2 * multiplier * atr
        else:
            stop = entry_price + multiplier * atr
            tp = entry_price - 2 * multiplier * atr
        return LayerOutput(
            id=f"risk_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="RiskEngine",
            semantic_type="Risk", confidence=0.9, valid=True,
            evidence=[f"Stop: {stop}, TP: {tp}"],
            payload={"stop_loss": stop, "take_profit": tp, "risk_reward": 2.0}
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["RiskEngine dimensiona risco da operação."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
