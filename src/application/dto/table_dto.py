from dataclasses import dataclass


@dataclass
class TableCreateDTO:
    """DTO для создания столика (передача между слоями)"""
    name: str
    seats: int
    location: str


@dataclass
class TableDTO:
    """DTO для передачи данных о столике"""
    id: int
    name: str
    seats: int
    location: str
