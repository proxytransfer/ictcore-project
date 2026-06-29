from typing import Any, Dict, List
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class IFVGEngine(MotorICT):
    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        fvg_data = context.get('fvg')
        if not fvg_data or not fvg_data.valid:
            return LayerOutput(
                id=f"ifvg_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name="IFVGEngine",
                semantic_type="IFVG", confidence=0.0, valid=False,
                evidence=["FVG original não disponível"]
            )
        current_price = context.get('current_price', 0)
        upper = fvg_data.payload.get('upper', 0)
        lower = fvg_data.payload.get('lower', 0)
        if upper and lower:
            if (fvg_data.payload.get('type') == 'bullish' and current_price < lower) or \
               (fvg_data.payload.get('type') == 'bearish' and current_price > upper):
                return LayerOutput(
                    id=f"ifvg_{datetime.now().timestamp()}",
                    timestamp=datetime.now(), layer_name="IFVGEngine",
                    semantic_type="IFVG", confidence=0.7, valid=True,
                    evidence=["FVG invertido (IFVG)"],
                    payload={"original_fvg": fvg_data.payload, "inverted": True}
                )
        return LayerOutput(
            id=f"ifvg_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="IFVGEngine",
            semantic_type="IFVG", confidence=0.0, valid=False,
            evidence=["FVG não invertido"]
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["IFVGEngine monitora inversão de FVGs."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
