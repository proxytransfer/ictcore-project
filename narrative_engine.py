from typing import Any, Dict, List
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class NarrativeEngine(MotorICT):
    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        bias = context.get('bias')
        draw = context.get('draw')
        po3 = context.get('po3')
        parts = []
        if bias and bias.valid:
            parts.append(f"Bias {bias.payload.get('bias')}")
        if draw and draw.valid:
            parts.append(f"Draw on {draw.payload.get('direction')}")
        if po3 and po3.valid:
            parts.append(f"PO3 manipulação {po3.payload.get('manipulation')}")
        narrative = " → ".join(parts) if parts else "Narrativa indefinida"
        return LayerOutput(
            id=f"narr_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="NarrativeEngine",
            semantic_type="Narrative", confidence=0.8 if parts else 0.2, valid=bool(parts),
            evidence=[narrative],
            payload={"narrative": narrative, "components": parts}
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["NarrativeEngine descreve o que o mercado está tentando fazer."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
