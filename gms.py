mport json
import os
from abc import ABC, abstractmethod


class Car(ABC):
    def __init__(self, car_number, full_name, age, racing_team, speed, capacity):  #'using double underscore for private attributes '
        self.car_number = car_number
        self.full_name = full_name
        self.age = age
        self.racing_team = racing_team
        self.speed = speed
        self.capacity = capacity

    # 'attributes encapsulation'
    #'using @property in python (getter and setter)'
    #"car number"
    @property
    def car_number(self) -> str:
        return self._car_number

    @car_number.setter
    def car_number(self, value):
        number = str(value).strip()  #"to properly clean when reading from file"
        if not number:
            raise ValueError("Enter the car number")
        self._car_number = number

    # full name
    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        name = str(value).strip()
        if not name:
            raise ValueError("Enter the car name")
        self._full_name = name

    # age
    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value):
        Age = int(value)
        if Age < 0:
            raise ValueError("Age should be a positive integer")
        self._age = Age

    # racing team
    @property
    def racing_team(self) -> str:
        return self._racing_team

    @racing_team.setter
    def racing_team(self, value):
        team = str(value).strip()
        if not team:
            raise ValueError("Enter the team ")
        self._racing_team = team

    # speed
    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, value):
        Speed = float(value)
        if Speed <= 0:
            raise ValueError("Enter a speed value")
        self._speed = Speed

    # capacity
    @property
    def capacity(self) -> float:
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        cap = float(value)
        if cap <= 0:
            raise ValueError("Enter a capacity value")
        self._capacity = cap

    # Methods
    @abstractmethod
    def per_score(self) -> float:
        pass

    @abstractmethod
    def car_details(self) -> dict:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass


# SUBCLASSES
class Racer(Car):
    def __init__(
        self,
        car_number,
        full_name,
        age,
        racing_team,
        speed,
        capacity,
        races_completed,
        laps_completed,
    ):
        super().__init__(car_number, full_name, age, racing_team, speed, capacity)
        self.races_completed = races_completed
        self.laps_completed = laps_completed

    @property
    def races_completed(self) -> int:
        return self._races_completed

    @races_completed.setter
    def races_completed(self, value):
        val = int(value)
        if val < 0:
            raise ValueError("Enter a positive value")
        self._races_completed = val

    @property
    def laps_completed(self) -> int:
        return self._laps_completed

    @laps_completed.setter
    def laps_completed(self, value):
        val = int(value)
        if val < 0:
            raise ValueError("Enter a positive value")
        self._laps_completed = val

    def per_score(self) -> float:
        return (self.speed * 10) + (self.capacity * 1)

    def car_details(self) -> dict:
        return {
            "races_completed": self.races_completed,
            "laps_completed": self.laps_completed,
        }

    def to_dict(self) -> dict:
        return {
            "type": "Racer",
            "car_number": self.car_number,
            "full_name": self.full_name,
            "age": self.age,
            "racing_team": self.racing_team,
            "speed": self.speed,
            "capacity": self.capacity,
            "extra_attributes": {
                "races_completed": self.races_completed,
                "laps_completed": self.laps_completed,
            },
        }


class SupportVehicle(Car):
    def __init__(
        self,
        car_number,
        full_name,
        age,
        racing_team,
        speed,
        capacity,
        crew_size,
        reliability_rating,
    ):
        super().__init__(car_number, full_name, age, racing_team, speed, capacity)
        self.crew_size = crew_size
        self.reliability_rating = reliability_rating

    @property
    def crew_size(self) -> int:
        return self._crew_size

    @crew_size.setter
    def crew_size(self, value: int):
        val = int(value)
        if val < 1:
            raise ValueError("Crew size must be at least 1.")
        self._crew_size = val

    @property
    def reliability_rating(self) -> float:
        return self._reliability_rating

    @reliability_rating.setter
    def reliability_rating(self, value: float):
        val = float(value)
        if not (0.0 <= val <= 10.0):
            raise ValueError("Reliability rating must be between 0.0 and 10.0.")
        self._reliability_rating = val

    def per_score(self) -> float:
        # Support Formula: (Speed * 5) + (Capacity * 5)
        return (self.speed * 5) + (self.capacity * 5)

    def car_details(self) -> dict:
        return {
            "crew_size": self.crew_size,
            "reliability_rating": self.reliability_rating,
        }

    def to_dict(self) -> dict:
        return {
            "type": "SupportVehicle",
            "car_number": self.car_number,
            "full_name": self.full_name,
            "age": self.age,
            "racing_team": self.racing_team,
            "speed": self.speed,
            "capacity": self.capacity,
            "extra_attributes": {
                "crew_size": self.crew_size,
                "reliability_rating": self.reliability_rating,
            },
        }
