from typing import Literal, Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class TaskDeadlineChangedResponse:
    status: Literal["success", "error"]
    deadline: Optional[datetime] = None
    error: Optional[str] = None
