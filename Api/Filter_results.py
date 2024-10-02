import json
from typing import Optional

class FilterResults:
    def __init__(self, filtered: bool, severity: Optional[str] = None, detected: Optional[bool] = None):
        self.filtered = filtered
        self.severity = severity
        self.detected = detected
