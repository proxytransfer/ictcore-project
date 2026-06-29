from typing import List
import pandas as pd
from core.interfaces import Detector
from core.models import MarketEvent, SemanticEvent, LayerOutput
from core.interfaces import MotorICT

class MotorDetectorAdapter(Detector):
    """Adaptador que transforma um MotorICT em um Detector padrão."""
    def __init__(self, motor: MotorICT, required_concepts: List[str] = None):
        self.motor = motor
        self._required = required_concepts or []

    def required_concepts(self) -> List[str]:
        return self._required

    async def detect(self, events: List[MarketEvent]) -> List[SemanticEvent]:
        if not events:
            return []
        # Constrói o DataFrame
        df = pd.DataFrame([e.dict() for e in events])
        if 'timestamp' in df.columns:
            df.set_index('timestamp', inplace=True)
        # Contexto mínimo: dados OHLCV e preço atual
        context = {
            'data': df,
            'current_price': float(df['close'].iloc[-1]) if 'close' in df.columns else 0.0,
            'symbol': events[0].symbol
        }
        # Executa o motor
        try:
            output: LayerOutput = self.motor.analyze(context)
        except Exception as e:
            return []
        if output.valid:
            # Converte para SemanticEvent
            event = output.to_semantic_event(events[0].symbol)
            # Se houver dados de evidence do motor, tenta transformar em MarketEvent (simplificado)
            # Aqui não convertemos, pois os motores não retornam MarketEvents.
            return [event]
        return []
