from dataclasses import dataclass
from typing import Literal
from datetime import datetime


@dataclass
class TaskDeadlineChanged:
    status: Literal["success", "error"]
    deadline: datetime = None
    error: str = None
