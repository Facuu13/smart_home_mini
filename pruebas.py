from models import Sensor, Relay
from home import SmartHome

home = SmartHome()

temp_living = Sensor("sensor_1", "Temp living", "living", "temperature", "°C")
temp_living.update_value(24.5)

luz_living = Relay("relay_1", "Luz living", "living", False, "Luz techo")

home.add_device(temp_living)
home.add_device(luz_living)

print(home.to_dict())
