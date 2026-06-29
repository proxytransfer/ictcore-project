from typing import Any, Dict, List
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class LiquidityEngine(MotorICT):
    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        external = context.get('external_liquidity')
        internal = context.get('internal_liquidity')
        if not external and not internal:
            return LayerOutput(
                id=f"liq_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name="LiquidityEngine",
                semantic_type="Liquidity", confidence=0.0, valid=False,
                evidence=["Nenhum dado de liquidez"]
            )
        combined = {"external": external, "internal": internal}
        return LayerOutput(
            id=f"liq_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="LiquidityEngine",
            semantic_type="Liquidity", confidence=0.9, valid=True,
            evidence=["Liquidez mapeada"],
            payload=combined
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["LiquidityEngine consolida níveis de liquidez."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
