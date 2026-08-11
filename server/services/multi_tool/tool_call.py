from dataclasses import dataclass, field
from typing import Callable


@dataclass
class ToolCall:
    tool: Callable
    args: dict = field(default_factory=dict)