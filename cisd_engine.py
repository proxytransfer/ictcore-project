from typing import Any, Dict, List
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class CISDEngine(MotorICT):
    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        mss = context.get('mss')
        new_swings = context.get('new_swings', [])
        if not mss or not mss.valid:
            return LayerOutput(
                id=f"cisd_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name="CISDEngine",
                semantic_type="CISD", confidence=0.0, valid=False,
                evidence=["MSS ausente"]
            )
        direction = mss.payload.get('type')
        count = sum(1 for s in new_swings if s.get('direction') == direction)
        trending = count >= 2
        return LayerOutput(
            id=f"cisd_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="CISDEngine",
            semantic_type="CISD", confidence=0.8 if trending else 0.4, valid=trending,
            evidence=[f"CISD {'confirmado' if trending else 'pendente'}"],
            payload={"state": "trending" if trending else "ranging", "new_swings": count}
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["CISDEngine avalia mudança no regime de entrega."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
