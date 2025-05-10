from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab5.app import Application


@dataclass
class BaseAccessor:
    app: "Application"
