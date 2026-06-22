from pydantic import BaseModel

class AnomalyResponse(BaseModel):
    total_records: int
    anomalies_found: int
    anomalies: list