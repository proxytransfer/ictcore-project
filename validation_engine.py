from typing import Any, Dict, List
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class ValidationEngine(MotorICT):
    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        outputs = context.get('layer_outputs', [])
        conflicts = []
        mss = next((o for o in outputs if o.semantic_type == 'MSS'), None)
        choch = next((o for o in outputs if o.semantic_type == 'CHOCH'), None)
        if mss and choch and mss.valid and choch.valid:
            conflicts.append("MSS e CHOCH conflitantes")
        valid = len(conflicts) == 0
        return LayerOutput(
            id=f"val_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="ValidationEngine",
            semantic_type="Validation", confidence=1.0 if valid else 0.5, valid=valid,
            evidence=conflicts if conflicts else ["Sem conflitos"],
            payload={"conflicts": conflicts}
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["ValidationEngine checa consistência ontológica."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
