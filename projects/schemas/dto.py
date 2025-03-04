from enum import Enum
from dataclasses import dataclass


@dataclass
class User:
    id: int
    permissions: list[str]


class Role(Enum):
    ADMIN = "admin"
    USER = "user"
