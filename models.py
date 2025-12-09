from datetime import datetime
from typing import Optional

class Device:
    def __init__(self, device_id: str, name: str, room_name: str):
        self.device_id = device_id
        self.name = name
        self.room_name = room_name
        self.online = True
        self.last_value_at: Optional[datetime] = None

    def to_dict(self):
        return {
            "device_id": self.device_id,
            "name": self.name,
            "room_name": self.room_name,
            "online": self.online,
            "last_value_at": self.last_value_at.isoformat() if self.last_value_at else None
        }

class Sensor(Device):
    def __init__(self, device_id: str, name: str, room_name: str, sensor_type: str, unit: str):
        super().__init__(device_id, name, room_name)
        self.sensor_type = sensor_type
        self.unit = unit
        self.value: Optional[float] = None

    def update_value(self, new_value: float):
        self.value = new_value
        self.last_value_at = datetime.now()
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "type": "sensor",
            "sensor_type": self.sensor_type,
            "unit": self.unit,
            "value": self.value
        })
        return base_dict

class Relay(Device):
    def __init__(self, device_id: str, name: str, room_name: str, state: bool, load_name: str):
        super().__init__(device_id, name, room_name)
        self.state = state  
        self.load_name = load_name
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "type": "relay",
            "state": self.state,
            "load_name": self.load_name
        })
        return base_dict
    
    def turn_on(self):
        self.state = True
    
    def turn_off(self):
        self.state = False
    
    def toggle(self):
        self.state = not self.state

