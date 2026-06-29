from typing import Any, Dict, List
import pandas as pd
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class SwingEngine(MotorICT):
    def __init__(self, left_bars: int = 3, right_bars: int = 3):
        self.left_bars = left_bars
        self.right_bars = right_bars

    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        data: pd.DataFrame = context.get('data')
        if data is None or len(data) < self.left_bars + self.right_bars + 1:
            return LayerOutput(
                id=f"swing_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name="SwingEngine",
                semantic_type="Swing", confidence=0.0, valid=False,
                evidence=["Dados insuficientes"]
            )
        swings = []
        for i in range(self.left_bars, len(data) - self.right_bars):
            if data['high'].iloc[i] == data['high'].iloc[i - self.left_bars:i + self.right_bars + 1].max():
                swings.append({'type': 'high', 'price': float(data['high'].iloc[i]), 'index': i})
            if data['low'].iloc[i] == data['low'].iloc[i - self.left_bars:i + self.right_bars + 1].min():
                swings.append({'type': 'low', 'price': float(data['low'].iloc[i]), 'index': i})
        return LayerOutput(
            id=f"swing_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="SwingEngine",
            semantic_type="Swing", confidence=1.0 if swings else 0.3, valid=bool(swings),
            evidence=[f"Encontrados {len(swings)} swings"],
            payload={"swings": swings}
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid and len(output.payload.get('swings', [])) > 0

    def explain(self, output: LayerOutput) -> List[str]:
        return [f"SwingEngine detectou {len(output.payload.get('swings', []))} pivots estruturais."]

    def metrics(self) -> Dict[str, float]:
        return {"swing_count": 0.0}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return {"swings": output.payload.get('swings')}
