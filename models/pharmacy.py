"""
Model domenowy „Apteka”.
Każdy obiekt ląduje w liście _registry, aby łatwo go pobierać z innych miejsc.
"""
from services.geolocation import get_coordinates

class Pharmacy:
    _registry: list["Pharmacy"] = []

    def __init__(self, name: str, city: str):
        self.name = name.title()
        self.city = city.title()
        self.coordinates = get_coordinates(self.city)
        self.marker = None
        Pharmacy._registry.append(self)

    @classmethod
    def all(cls) -> list["Pharmacy"]:
        return cls._registry

    @classmethod
    def get_all_instances(cls) -> list["Pharmacy"]:
        return cls._registry

    def update(self, name: str, city: str) -> None:
        self.name = name.title()
        self.city = city.title()
        self.coordinates = get_coordinates(self.city)