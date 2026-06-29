from datetime import datetime, time
import pytz
from core.interfaces import MotorICT
from core.models import LayerOutput

class KillZoneEngine(MotorICT):
    def __init__(self, tz='US/Eastern'):
        self.tz = pytz.timezone(tz)
        self.kill_zones = {
            'London Open': (time(2,0), time(5,0)),
            'NY Open': (time(8,0), time(9,0)),
            'London Close': (time(10,0), time(11,0)),
        }

    def analyze(self, context: dict = None) -> LayerOutput:
        now = datetime.now(self.tz).time()
        active = None
        for name, (start, end) in self.kill_zones.items():
            if start <= now < end:
                active = name
                break
        return LayerOutput(
            id=f"kz_{datetime.now().timestamp()}",
            timestamp=datetime.now(), layer_name="KillZoneEngine",
            semantic_type="KillZone", confidence=1.0, valid=True,
            evidence=[f"Kill Zone: {active}" if active else "Fora de Kill Zone"],
            payload={"active": active is not None, "name": active}
        )

    def validate(self, output: LayerOutput) -> bool:
        return output.valid

    def explain(self, output: LayerOutput) -> List[str]:
        return ["KillZoneEngine indica janelas de alta atividade."]

    def metrics(self) -> Dict[str, float]:
        return {}

    def audit(self, output: LayerOutput) -> Dict[str, Any]:
        return output.payload
