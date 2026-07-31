import json
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


# garage management functions to be used in MENU
class garageManager:
    def __init__(self, file="radiator_springs_garage.json"):
        self.file = file  # get the JSON file
        self._cars = {}  # empty dictionary to link each car to its attributes like number ,speed ,etc
        self.loadfromfile()

    def carNumCheck(self, car_number) -> bool:
        return str(car_number).strip() in self._cars

    def check_in_car(self, car: Car) -> bool:
        if self.carNumCheck(car.car_number):
            raise ValueError("Number already exists")
        # if not then add  it in dictionary and save in the file
        self._cars[car.car_number] = car
        self.saveToFile()
        return True

    def find_car(self, car_number: str):
        return self._cars.get(str(car_number).strip())

    def viewallcars(self) -> list:
        return list(self._cars.values())

    def carRetire(self, car_number) -> bool:
        num = str(car_number).strip()
        if num in self._cars:
            del self._cars[num]
            self.saveToFile()
            return True
        return False

    def reportCars(self) -> dict:
        cars = self.viewallcars()
        if not cars:
            return {
                "Cars checked in": 0,
                "average score": 0.0,
                "breakdown of each car": {},
            }  # returns a dictionary
        numofcars = len(cars)  # the length of the dict
        averagePerformance = (
            sum(i.per_score() for i in cars) / numofcars
        )
        teams = {}  # will store the breakdown of each team to be displayed
        for i in cars:
            teams[i.racing_team] = teams.get(i.racing_team, 0) + 1

        return {
            "Cars checked in": numofcars,
            "average score": averagePerformance,
            "breakdown of each care": teams,
        }

    # handling the files and their functitons

    def saveToFile(self):
        data = [car.to_dict() for car in self._cars.values()]
        with open(self.file, "w") as file:
            json.dump(data, file, indent=4)

    def loadfromfile(self):
        if not os.path.isfile(self.file):
            return  # to prevent file not found error

        try:
            with open(self.file, "r") as file:
                data = json.load(file)
            for item in data:
                car = None
                if item.get("type") == "Racer":
                    car = Racer(
                        car_number=item["car_number"],
                        full_name=item["full_name"],
                        age=item["age"],
                        racing_team=item["racing_team"],
                        speed=item["speed"],
                        capacity=item["capacity"],
                        races_completed=item.get("extra_attributes", {}).get("races_completed", 0),  # extra
                        laps_completed=item.get("extra_attributes", {}).get("laps_completed", 0),
                    )
                elif item.get("type") == "SupportVehicle":
                    car = SupportVehicle(
                        car_number=item["car_number"],
                        full_name=item["full_name"],
                        age=item["age"],
                        racing_team=item["racing_team"],
                        speed=item["speed"],
                        capacity=item["capacity"],
                        crew_size=item.get("extra_attributes", {}).get("crew_size", 1),  # extra
                        reliability_rating=item.get("extra_attributes", {}).get("reliability_rating", 10.0),
                    )
                if car:
                    self._cars[car.car_number] = car
        except Exception as e:
            print(f"Error loading file: {e}")
            
            
#the main menu             
            
 def main():
     while True:
         print("\n===RADIATOR SPRINGS GARAGE MANAGER===")
        print("1. Check In New Vehicle")
        print("2. Search Vehicle by Number")
        print("3. View All Vehicles")
        print("4. Retire Vehicle")
        print("5. Generate Garage Report")
        print("6. Exit")
     
        choice = input("Select an Option ")  
        if(choice == 1):
            vehicleType = input("Enter the vehicle type 1.Racer 2.Vehicle support")
            try:
                num = input("Car Number: ").strip()
                name = input("Full Name: ").strip()
                age = input("Age: ").strip()
                team = input("Racing Team: ").strip()
                speed = input("Speed: ").strip()
                cap = input("Capacity: ").strip()        
              
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
 
            