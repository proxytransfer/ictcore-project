from typing import Any, Dict, List
import pandas as pd
from datetime import datetime
from core.interfaces import MotorICT
from core.models import LayerOutput

class QuarterlyEngine(MotorICT):
    def analyze(self, context: Dict[str, Any]) -> LayerOutput:
        data: pd.DataFrame = context.get('monthly_data')
        if data is None or len(data) < 3:
            return LayerOutput(
                id=f"qt_{datetime.now().timestamp()}",
                timestamp=datetime.now(), layer_name="QuarterlyEngine",
                semantic_type="QuarterlyTheory", confidence=0.0, valid=False,
                evidence=["Dados mensais insuficientes"]
            )
        quarter_open = data.iloc[0]['open']
        last_close = data.iloc[-1]['close']
        bias = "bullish" if last_close > quarter_open else "bearish"
        alignment = self._fractal(data, bias)
        return LayerOutput(
            id=f"qt_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="QuarterlyEngine",
            semantic_type="QuarterlyTheory", confidence=alignment, valid=alignment > 0.5,
            evidence=[f"Viés trimestral {bias}"],
            payload={"bias": bias, "fractal_alignment": alignment, "quarter_open": float(quarter_open)}
        )

    def _fractal(self, data, bias):
        recent = data.tail(4)
        if bias == 'bullish':
            return sum(recent['close'] > recent['open']) / 4
        else:
            return sum(recent['close'] < recent['open']) / 4

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["QuarterlyEngine define contexto trimestral."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
