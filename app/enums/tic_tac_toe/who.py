from enum import Enum


class Who(Enum):
    X = -1
    B = 0
    O = 1  # noqa

    def text(self) -> str:
        if self == Who.X:
            return "✖️"
        if self == Who.O:
            return "🟢"
        return "❓"
