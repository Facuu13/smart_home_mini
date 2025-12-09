from models import Device, Sensor, Relay

class SmartHome:
    def __init__(self):
        self.devices: dict[str, Device] = {}

    def add_device(self, device: Device):
        self.devices[device.device_id] = device
    
    def get_device(self, device_id: str) -> Device:
        return self.devices.get(device_id)

    def get_devices_by_room(self, room_name: str) -> list[Device]:
        return [device for device in self.devices.values() if device.room_name == room_name]
    
    def to_dict(self):
        # Representación de toda la casa para guardar en JSON
        return {
            "devices": [d.to_dict() for d in self.devices.values()]
        }