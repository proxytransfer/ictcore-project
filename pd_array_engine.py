from typing import Any, Dict, List
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class PDArrayEngine(MotorICT):
    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        arrays = {}
        for key in ['fvg', 'order_block', 'breaker', 'mitigation', 'ifvg']:
            val = context.get(key)
            if val and val.valid:
                arrays[key] = val.payload
        return LayerOutput(
            id=f"pda_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="PDArrayEngine",
            semantic_type="PDArray", confidence=0.9 if arrays else 0.0, valid=bool(arrays),
            evidence=[f"PD Arrays encontrados: {list(arrays.keys())}"],
            payload={"arrays": arrays}
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["PDArrayEngine consolida arrays de preço."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
