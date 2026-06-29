from typing import Any, Dict, List
import pandas as pd
import numpy as np
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class DisplacementEngine(MotorICT):
    def __init__(self, min_body_ratio: float = 0.7, atr_period: int = 14):
        self.min_body_ratio = min_body_ratio
        self.atr_period = atr_period

    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        data: pd.DataFrame = context.get('data')
        if data is None or len(data) < self.atr_period:
            return LayerOutput(
                id=f"disp_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name="DisplacementEngine",
                semantic_type="Displacement", confidence=0.0, valid=False,
                evidence=["Dados insuficientes"]
            )
        high, low, close = data['high'], data['low'], data['close']
        tr = np.maximum(high - low, np.maximum(abs(high - close.shift()), abs(low - close.shift())))
        atr = float(tr.rolling(self.atr_period).mean().iloc[-1])
        displacements = []
        for i in range(1, len(data)):
            body = abs(data['close'].iloc[i] - data['open'].iloc[i])
            range_i = data['high'].iloc[i] - data['low'].iloc[i]
            if range_i > 0 and body / range_i >= self.min_body_ratio and range_i > 0.5 * atr:
                direction = 'bullish' if data['close'].iloc[i] > data['open'].iloc[i] else 'bearish'
                displacements.append({'index': i, 'direction': direction, 'body_ratio': float(body/range_i)})
        latest = displacements[-1] if displacements else None
        return LayerOutput(
            id=f"disp_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="DisplacementEngine",
            semantic_type="Displacement", confidence=0.9 if latest else 0.2, valid=latest is not None,
            evidence=[f"Deslocamento {latest['direction']}" if latest else "Sem deslocamento"],
            payload={"displacements": displacements, "latest": latest, "atr": atr}
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["DisplacementEngine avalia impulsos direcionais."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
