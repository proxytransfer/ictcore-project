from typing import Any, Dict, List
import pandas as pd
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class PO3Engine(MotorICT):
    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        data: pd.DataFrame = context.get('session_data')
        if data is None or len(data) < 6:
            return LayerOutput(
                id=f"po3_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name="PO3Engine",
                semantic_type="PO3", confidence=0.0, valid=False,
                evidence=["Dados insuficientes para PO3"]
            )
        first_high = data['high'].iloc[0]
        first_low = data['low'].iloc[0]
        last_high = data['high'].max()
        last_low = data['low'].min()
        manipulation = None
        if last_low < first_low and data['close'].iloc[-1] > first_low:
            manipulation = "down"
        elif last_high > first_high and data['close'].iloc[-1] < first_high:
            manipulation = "up"
        return LayerOutput(
            id=f"po3_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="PO3Engine",
            semantic_type="PO3", confidence=0.7 if manipulation else 0.3, valid=manipulation is not None,
            evidence=[f"Manipulação {manipulation}" if manipulation else "Sem manipulação"],
            payload={"accumulation_range": (float(first_high), float(first_low)), "manipulation": manipulation}
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["PO3Engine analisa acumulação, manipulação e distribuição."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
