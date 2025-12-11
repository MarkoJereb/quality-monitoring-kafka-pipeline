from jsonschema import validate

QUALITY_SCHEMA = {
    "type": "object",
    "properties": {
        "ts": {"type": "string", "format": "date-time"},
        "temperature": {"type": "number"},
        "ph": {"type": "number"},
        "moisture": {"type": "number"}
    },
    "required": ["ts", "temperature", "ph", "moisture"]
}

def validate_message(msg: dict):
    validate(instance=msg, schema=QUALITY_SCHEMA)
