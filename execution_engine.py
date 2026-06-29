from typing import Any, Dict, List
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class ExecutionEngine(MotorICT):
    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        checks = context.get('checks', {})
        passed = sum(1 for v in checks.values() if v)
        total = len(checks)
        signal = "buy" if context.get('bias') == 'bullish' else "sell"
        return LayerOutput(
            id=f"exec_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="ExecutionEngine",
            semantic_type="EntrySignal", confidence=passed/total if total else 0,
            valid=passed >= 8,
            evidence=[f"Checks: {passed}/{total}"],
            payload={"direction": signal, "entry_price": context.get('current_price'), "checks": checks}
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["ExecutionEngine decide entrada com checklist."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
