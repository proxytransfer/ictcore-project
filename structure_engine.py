from typing import Any, Dict, List
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class StructureEngine(MotorICT):
    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        pivots = context.get('pivots', [])
        if len(pivots) < 2:
            return LayerOutput(
                id=f"struct_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name="StructureEngine",
                semantic_type="Structure", confidence=0.0, valid=False,
                evidence=["Pivots insuficientes"]
            )
        last_high = next((p for p in reversed(pivots) if p['type'] == 'high'), None)
        last_low = next((p for p in reversed(pivots) if p['type'] == 'low'), None)
        if last_high and last_low:
            structure = "bullish" if last_high['price'] > last_low['price'] else "bearish"
        else:
            structure = "neutral"
        return LayerOutput(
            id=f"struct_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="StructureEngine",
            semantic_type="Structure", confidence=0.8, valid=True,
            evidence=[f"Estrutura: {structure}"],
            payload={"structure": structure, "last_high": last_high, "last_low": last_low}
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return [f"Estrutura atual: {output.payload.get('structure')}."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
