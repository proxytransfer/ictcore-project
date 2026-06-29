from typing import Any, Dict, List
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class MitigationEngine(MotorICT):
    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        fvg = context.get('fvg')
        ob = context.get('order_block')
        current_price = context.get('current_price')
        mitigated = False
        target = None
        if fvg and fvg.valid:
            upper = fvg.payload.get('upper', 0)
            lower = fvg.payload.get('lower', 0)
            if (fvg.payload.get('type') == 'bullish' and current_price <= lower) or \
               (fvg.payload.get('type') == 'bearish' and current_price >= upper):
                mitigated = True
                target = 'fvg'
        if not mitigated and ob and ob.valid:
            ob_high = ob.payload['high']
            ob_low = ob.payload['low']
            if ob_low <= current_price <= ob_high:
                mitigated = True
                target = 'order_block'
        return LayerOutput(
            id=f"mit_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="MitigationEngine",
            semantic_type="Mitigation", confidence=0.8 if mitigated else 0.2, valid=mitigated,
            evidence=[f"Mitigação em {target}" if mitigated else "Sem mitigação"],
            payload={"mitigated": mitigated, "target": target}
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["MitigationEngine acompanha a entrega de preço aos PD Arrays."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
