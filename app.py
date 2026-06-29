from fastapi import FastAPI, Depends
from core.container import Container
from core.models import MarketEvent

app = FastAPI()
container = Container()

@app.get("/symbols/{symbol}/candles")
async def get_candles(symbol: str, start: str, end: str):
    provider = container.provider()
    await provider.connect()
    events = []
    async for ev in provider.get_candles(symbol, start, end):
        events.append(ev.dict())
    return events

@app.get("/detect/{engine_name}")
async def detect(engine_name: str, symbol: str):
    detector = container.get_detector(engine_name)
    if not detector:
        return {"error": "Detector not found"}
    # Supõe que exista um armazenamento de eventos recentes; aqui seria uma consulta ao cache.
    recent_events: List[MarketEvent] = []  # mock
    result = await detector.detect(recent_events)
    return [r.dict() for r in result]

@app.get("/hypotheses")
async def get_hypotheses(symbol: str):
    engine = container.inference_engine()
    # Buscar eventos do cache/eventbus...
    hypotheses = await engine.infer([], [])
    return [h.dict() for h in hypotheses]
