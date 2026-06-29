from datetime import datetime, time
import pytz
from core.interfaces import MotorICT
from core.models import LayerOutput

class SessionEngine(MotorICT):
    def __init__(self, tz='US/Eastern'):
        self.tz = pytz.timezone(tz)
        self.sessions = {
            'Asian': (time(20,0), time(3,0)),
            'London': (time(3,0), time(7,0)),
            'NY': (time(8,0), time(12,0)),
            'London_Close': (time(10,0), time(12,0)),
        }

    def analyze(self, context: dict = None) -> LayerOutput:
        now = datetime.now(self.tz).time()
        current = 'Asian'
        for sess, (start, end) in self.sessions.items():
            if start <= now < end:
                current = sess
                break
        return LayerOutput(
            id=f"sess_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="SessionEngine",
            semantic_type="Session", confidence=1.0, valid=True,
            evidence=[f"Sessão: {current}"],
            payload={"session": current}
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["SessionEngine define o período de negociação."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
