from datetime import datetime
from dataclasses import dataclass

@dataclass
class ReservationCreateDTO:
    """DTO для создания брони (передача между слоями)"""
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int

@dataclass
class ReservationDTO:
    """DTO для передачи данных о брони"""
    id: int
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int