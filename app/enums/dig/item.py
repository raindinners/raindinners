from enum import Enum


class Item(str, Enum):
    PLANT = "🌱"
    GROUND = "🪹"
    STONE = "🪨"
    USED = "💥"
    DIAMOND = "💎"
