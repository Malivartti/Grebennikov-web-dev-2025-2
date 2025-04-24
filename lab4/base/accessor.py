from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab4.app import Application


@dataclass
class BaseAccessor:
    app: "Application"
