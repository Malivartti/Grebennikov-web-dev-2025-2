from dataclasses import dataclass


@dataclass
class UserCreate:
    login: str
    password: str
    last_name: str
    first_name: str
    middle_name: str | None
    role_id: int
