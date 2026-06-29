from typing import Any, Dict, List
import pandas as pd
import numpy as np
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class FVGEngine(MotorICT):
    def __init__(self, min_gap_atr_ratio: float = 0.1, atr_period: int = 14):
        self.min_gap_atr_ratio = min_gap_atr_ratio
        self.atr_period = atr_period

    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        data: pd.DataFrame = context.get('data')
        if data is None or len(data) < 3:
            return LayerOutput(
                id=f"fvg_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name="FVGEngine",
                semantic_type="FVG", confidence=0.0, valid=False,
                evidence=["Dados insuficientes"]
            )
        atr = self._atr(data)
        fvgs = []
        for i in range(2, len(data)):
            if data['low'].iloc[i-2] > data['high'].iloc[i]:
                gap = float(data['low'].iloc[i-2] - data['high'].iloc[i])
                if gap > self.min_gap_atr_ratio * atr:
                    fvgs.append({'type': 'bullish', 'upper': float(data['low'].iloc[i-2]), 'lower': float(data['high'].iloc[i]), 'quality': gap/atr})
            elif data['high'].iloc[i-2] < data['low'].iloc[i]:
                gap = float(data['low'].iloc[i] - data['high'].iloc[i-2])
                if gap > self.min_gap_atr_ratio * atr:
                    fvgs.append({'type': 'bearish', 'upper': float(data['low'].iloc[i]), 'lower': float(data['high'].iloc[i-2]), 'quality': gap/atr})
        latest = fvgs[-1] if fvgs else None
        return LayerOutput(
            id=f"fvg_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="FVGEngine",
            semantic_type="FVG", confidence=latest['quality'] if latest else 0.0, valid=latest is not None,
            evidence=[f"FVG {latest['type']} {latest['upper']}-{latest['lower']}" if latest else "Sem FVG"],
            payload={"fvgs": fvgs, "latest": latest}
        )

    def _atr(self, df):
        high, low, close = df['high'], df['low'], df['close']
        tr = np.maximum(high - low, np.maximum(abs(high - close.shift()), abs(low - close.shift())))
        return float(tr.rolling(self.atr_period).mean().iloc[-1])

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["FVGEngine identifica gaps de valor justo."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
