from core.models import MarketEvent

class Validator:
    def validate(self, event: MarketEvent) -> bool:
        return (event.high >= event.low and
                event.high >= event.open and
                event.high >= event.close and
                event.low <= event.open and
                event.low <= event.close)
