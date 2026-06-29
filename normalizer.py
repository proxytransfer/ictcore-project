from core.models import MarketEvent
from datetime import datetime

class Normalizer:
    def normalize(self, raw: dict, provider: str) -> MarketEvent:
        if provider == "yahoo":
            return MarketEvent(
                timestamp=raw.get('Date', datetime.now()),
                symbol=raw.get('symbol', 'UNKNOWN'),
                open=float(raw['Open']),
                high=float(raw['High']),
                low=float(raw['Low']),
                close=float(raw['Close']),
                volume=float(raw.get('Volume', 0.0)),
                provider="yahoo",
                quality=0.95,
                timezone="UTC"
            )
        raise ValueError(f"Provider desconhecido: {provider}")
