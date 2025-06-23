from services.geolocation import get_coordinates

class Customer:
    _registry: list["Customer"] = []

    def __init__(self, first: str, last: str, city: str, pharmacy: str):
        self.first_name = first.title()
        self.last_name = last.title()
        self.city = city.title()
        self.assigned_pharmacy = pharmacy
        self.coordinates = get_coordinates(self.city)
        self.marker = None
        Customer._registry.append(self)

    @classmethod
    def all(cls):
        return cls._registry

    @classmethod
    def get_all_instances(cls):
        return cls._registry

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def update(self, first, last, city, pharmacy):
        self.first_name = first.title()
        self.last_name = last.title()
        self.city = city.title()
        self.assigned_pharmacy = pharmacy
        self.coordinates = get_coordinates(self.city)