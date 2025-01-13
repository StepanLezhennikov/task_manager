from typing import Literal
from datetime import datetime
from dataclasses import dataclass


@dataclass
class TaskDeadlineChanged:
    status: Literal["success", "error"]
    deadline: datetime | None
    error: str | None
