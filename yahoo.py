import asyncio
import yfinance as yf
from datetime import datetime
from core.interfaces import BaseProvider
from core.models import MarketEvent

class YahooProvider(BaseProvider):
    def __init__(self):
        self._connected = False

    async def connect(self):
        self._connected = True

    async def disconnect(self):
        self._connected = False

    async def get_candles(self, symbol: str, start: datetime, end: datetime) -> AsyncIterator[MarketEvent]:
        if not self._connected:
            raise ConnectionError("Provider not connected")
        data = await asyncio.to_thread(yf.download, symbol, start=start, end=end, interval="1d")
        for idx, row in data.iterrows():
            yield MarketEvent(
                timestamp=idx.to_pydatetime(),
                symbol=symbol,
                open=float(row['Open']),
                high=float(row['High']),
                low=float(row['Low']),
                close=float(row['Close']),
                volume=float(row['Volume']) if 'Volume' in row else None,
                provider="yahoo",
                quality=0.95,
                timezone="UTC"
            )

    async def health(self) -> bool:
        return self._connected
