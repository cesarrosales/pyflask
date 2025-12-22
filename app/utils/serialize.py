from app.utils.json_safe import json_safe


def serialize_rows(rows):
    out = []
    for r in rows:
        data = dict(r._mapping) if hasattr(r, "_mapping") else dict(r)
        out.append({k: json_safe(v) for k, v in data.items()})
    return out
