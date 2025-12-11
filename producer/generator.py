import random
from datetime import datetime, timezone

def generate_reading():
    return {
        "ts": datetime.now(timezone.utc).isoformat(),
        "temperature": round(random.uniform(10.0, 40.0), 2),
        "ph": round(random.uniform(2.0, 9.0), 2),
        "moisture": round(random.uniform(0, 100), 2)
    }

if __name__ == "__main__":
    for _ in range(3):
        print(generate_reading())
