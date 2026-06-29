from typing import Any, Dict, List
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class BiasEngine(MotorICT):
    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        macro = context.get('macro')
        quarterly = context.get('quarterly')
        mss = context.get('mss')
        biases = []
        if macro and macro.valid:
            biases.append(macro.payload.get('bias'))
        if quarterly and quarterly.valid:
            biases.append(quarterly.payload.get('bias'))
        if mss and mss.valid:
            biases.append(mss.payload.get('type'))
        bullish = biases.count('bullish')
        bearish = biases.count('bearish')
        if bullish > bearish:
            bias = 'bullish'
        elif bearish > bullish:
            bias = 'bearish'
        else:
            bias = 'neutral'
        return LayerOutput(
            id=f"bias_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="BiasEngine",
            semantic_type="Bias", confidence=max(bullish, bearish)/len(biases) if biases else 0.0,
            valid=bias != 'neutral',
            evidence=[f"Viés consolidado: {bias}"],
            payload={"bias": bias, "components": biases}
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["BiasEngine combina vieses de diferentes timeframes."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
