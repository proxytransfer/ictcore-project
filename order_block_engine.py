from typing import Any, Dict, List
import pandas as pd
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class OrderBlockEngine(MotorICT):
    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        data: pd.DataFrame = context.get('data')
        displacement = context.get('displacement')
        if data is None or not displacement or not displacement.valid:
            return LayerOutput(
                id=f"ob_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name="OrderBlockEngine",
                semantic_type="OrderBlock", confidence=0.0, valid=False,
                evidence=["Dados ou deslocamento ausentes"]
            )
        latest_disp = displacement.payload.get('latest')
        if not latest_disp:
            return LayerOutput(
                id=f"ob_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name="OrderBlockEngine",
                semantic_type="OrderBlock", confidence=0.0, valid=False,
                evidence=["Sem deslocamento recente"]
            )
        idx = latest_disp['index']
        if idx > 0 and idx < len(data):
            ob_candle = data.iloc[idx-1]
            return LayerOutput(
                id=f"ob_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name="OrderBlockEngine",
                semantic_type="OrderBlock", confidence=0.8, valid=True,
                evidence=[f"Order Block em {ob_candle.name}"],
                payload={"high": float(ob_candle['high']), "low": float(ob_candle['low']), "direction": latest_disp['direction']}
            )
        return LayerOutput(
            id=f"ob_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="OrderBlockEngine",
            semantic_type="OrderBlock", confidence=0.0, valid=False,
            evidence=["Índice inválido"]
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["OrderBlockEngine identifica blocos de ordens."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
