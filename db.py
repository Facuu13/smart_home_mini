# db.py
from typing import Optional, List, Dict
from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "smart_home"
COLLECTION_NAME = "devices"


def get_collection():
    client = MongoClient(MONGO_URL)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]


def save_device(doc: dict) -> dict:
    """
    Guarda un dispositivo en Mongo.
    Usamos device_id como _id para que no se dupliquen.
    """
    col = get_collection()

    # Aseguramos que tenga _id
    if "device_id" in doc:
        doc["_id"] = doc["device_id"]

    # upsert: si ya existe, actualiza; si no, inserta
    col.replace_one({"_id": doc["_id"]}, doc, upsert=True)

    # Devolvemos el documento tal como quedó
    return doc


def list_devices() -> list[dict]:
    """
    Devuelve todos los dispositivos (sin el _id interno de Mongo
    si no lo querés exponer duplicado).
    """
    col = get_collection()
    docs = list(col.find({}))
    # Convertimos ObjectId si hiciera falta, pero como usamos _id = device_id, estamos bien.
    return docs


def get_device_by_id(device_id: str) -> Optional[dict]:
    col = get_collection()
    doc = col.find_one({"_id": device_id})
    return doc
