# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Literal

from db import save_device, list_devices, get_device_by_id

app = FastAPI()

# ---------- MODELOS Pydantic ----------

class DeviceCreate(BaseModel):
    device_id: str
    name: str
    room_name: str
    type: Literal["sensor", "relay"]
    sensor_type: Optional[str] = None
    unit: Optional[str] = None
    load_name: Optional[str] = None
    initial_state: Optional[bool] = None


class DeviceOut(BaseModel):
    device_id: str
    name: str
    room_name: str
    type: str
    sensor_type: Optional[str] = None
    unit: Optional[str] = None
    load_name: Optional[str] = None
    state: Optional[bool] = None
    value: Optional[float] = None
    online: bool
    last_value_at: Optional[str] = None


# ---------- ENDPOINTS ----------

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/devices", response_model=list[DeviceOut])
def get_devices():
    docs = list_devices()
    result = []

    for d in docs:
        result.append(DeviceOut(
            device_id=d["device_id"],
            name=d["name"],
            room_name=d["room_name"],
            type=d["type"],
            sensor_type=d.get("sensor_type"),
            unit=d.get("unit"),
            load_name=d.get("load_name"),
            state=d.get("state"),
            value=d.get("value"),
            online=d["online"],
            last_value_at=d.get("last_value_at"),
        ))

    return result


@app.get("/devices/{device_id}", response_model=DeviceOut)
def get_device(device_id: str):
    doc = get_device_by_id(device_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Device not found")

    return DeviceOut(
        device_id=doc["device_id"],
        name=doc["name"],
        room_name=doc["room_name"],
        type=doc["type"],
        sensor_type=doc.get("sensor_type"),
        unit=doc.get("unit"),
        load_name=doc.get("load_name"),
        state=doc.get("state"),
        value=doc.get("value"),
        online=doc["online"],
        last_value_at=doc.get("last_value_at"),
    )



@app.post("/devices", response_model=DeviceOut)
def create_device(payload: DeviceCreate):
    """
    Crea un nuevo dispositivo (sensor o relay) y lo guarda en MongoDB.
    """

    # 1) Armamos el documento base común
    doc = {
        "device_id": payload.device_id,
        "name": payload.name,
        "room_name": payload.room_name,
        "type": payload.type,
        "online": True,
        "last_value_at": None,
    }

    # 2) Campos específicos según el tipo
    if payload.type == "sensor":
        doc["sensor_type"] = payload.sensor_type
        doc["unit"] = payload.unit
        doc["value"] = None
        doc["state"] = None      # no aplica, pero lo dejamos explícito
        doc["load_name"] = None

    elif payload.type == "relay":
        doc["sensor_type"] = None
        doc["unit"] = None
        doc["value"] = None
        doc["load_name"] = payload.load_name
        doc["state"] = payload.initial_state if payload.initial_state is not None else False

    # 3) Guardar en Mongo
    saved = save_device(doc)

    # 4) Mapear a DeviceOut
    return DeviceOut(
        device_id=saved["device_id"],
        name=saved["name"],
        room_name=saved["room_name"],
        type=saved["type"],
        sensor_type=saved.get("sensor_type"),
        unit=saved.get("unit"),
        load_name=saved.get("load_name"),
        state=saved.get("state"),
        value=saved.get("value"),
        online=saved["online"],
        last_value_at=saved.get("last_value_at"),
    )
